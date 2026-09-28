import os
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tavily import TavilyClient
from firecrawl import FirecrawlApp

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
firecrawl = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))


def search_company(company_name: str) -> str:
    results = tavily.search(
        query=f"{company_name} company overview product services 2024",
        max_results=5
    )

    content = ""

    for r in results["results"]:
        content += f"Source: {r['url']}\n{r['content']}\n\n"

    return content


def scrape_website(url: str) -> str:
    try:
        result = firecrawl.scrape_url(
            url,
            params={"formats": ["markdown"]}
        )

        return result["markdown"][:3000]

    except Exception as e:
        return f"Website could not be scraped: {str(e)}"


def research_agent(state: dict) -> dict:
    company = state["company_name"]
    url = state["website_url"]

    print(f"🔍 Research Agent: Researching {company}...")

    search_results = search_company(company)
    website_content = scrape_website(url)

    prompt = f"""
    You are an expert business analyst.

    Company: {company}

    Website Content:
    {website_content}

    Search Results:
    {search_results}

    Extract the following information:

    1. What the company does (2-3 lines)
    2. Their main product or service
    3. Their target customer
    4. Current growth stage (startup / growing / enterprise)
    5. Any recent news or achievements

    IMPORTANT:
    - Be factual.
    - Do not invent information.
    - Only use information supported by the website content
      or search results.
    - If information is unavailable, leave it out.

    Be concise and respond in bullet points.
    """

    response = llm.invoke(prompt)

    clean = re.sub(
        r"<think>.*?</think>",
        "",
        response.content,
        flags=re.DOTALL
    ).strip()

    print("✅ Research complete!")

    return {
        "research": clean
    }


def pain_point_agent(state: dict) -> dict:
    print("🎯 Pain Point Agent: Identifying problems...")

    prompt = f"""
    You are an expert sales consultant.

    Company Research:
    {state["research"]}

    Our Service:
    {state["your_service"]}

    Based on the research:

    1. What are the top 3 potential pain points of this company?
    2. Which pain point does our service solve?
    3. What could be the cost of not solving this problem?

    IMPORTANT:
    - Base your analysis on the provided research.
    - Do not invent company facts.
    - Clearly distinguish potential problems from confirmed facts.

    Be specific and realistic.
    Respond in bullet points.
    """

    response = llm.invoke(prompt)

    clean = re.sub(
        r"<think>.*?</think>",
        "",
        response.content,
        flags=re.DOTALL
    ).strip()

    print("✅ Pain points identified!")

    return {
        "pain_points": clean
    }


def email_writer_agent(state: dict) -> dict:
    print("✍️ Email Writer Agent: Writing email...")

    prompt = f"""
    You are an expert cold email copywriter who writes
    professional and personalized cold emails.

    Company:
    {state["company_name"]}

    Research:
    {state["research"]}

    Pain Points:
    {state["pain_points"]}

    Our Service:
    {state["your_service"]}

    Sender Name:
    {state["your_name"]}

    Sender Role:
    {state["your_role"]}

    Previous Review:
    {state.get("review", "")}

    If a previous review exists, improve the email according
    to that feedback.

    ============================
    FACTUALITY PROTECTION
    ============================

    - Use ONLY facts explicitly supported by the Company Research.
    - Never invent statistics, revenue, percentages, growth numbers,
      clients, case studies, achievements, or business results.
    - Never claim that our service achieved a specific result unless
      that result is explicitly provided in the input.
    - Never create fake social proof.
    - Never invent customers or previous projects.
    - Never make unsupported claims about the company.
    - If a useful fact is not available, simply leave it out.
    - General reasoning about potential business problems is allowed,
      but present it as a possibility, not as a confirmed fact.

    ============================
    PERSONALIZATION
    ============================

    - This email is being written for the company,
      not a specific person.
    - Do NOT use placeholders such as:
      [First Name], [Name], [Recipient], [Company Name]
    - Address the company naturally.
    - Use the actual company name where appropriate.

    ============================
    EMAIL RULES
    ============================

    - Maximum 150 words.
    - Conversational and professional tone.
    - Do not start with "I".
    - No spam words.
    - No thinking.
    - No reasoning.
    - No explanation.
    - Output ONLY the email.

    Use exactly this format:

    SUBJECT: write subject here

    EMAIL:
    write email body here
    """

    response = llm.invoke(prompt)

    clean = re.sub(
        r"<think>.*?</think>",
        "",
        response.content,
        flags=re.DOTALL
    ).strip()

    # Remove unwanted placeholders if the model still generates them
    clean = re.sub(
        r"\[(First Name|Name|Recipient|Company Name)\]",
        state["company_name"],
        clean,
        flags=re.IGNORECASE
    )

    print(f"\n📨 Raw Email Output:\n{clean}\n")

    subject = ""
    body = ""

    lines = clean.split("\n")

    for i, line in enumerate(lines):

        if line.strip().startswith("SUBJECT:"):
            subject = line.replace("SUBJECT:", "").strip()

        elif line.strip().startswith("EMAIL:"):
            body = "\n".join(lines[i + 1:]).strip()
            break

    print("✅ Email ready!")

    return {
        "email_subject": subject,
        "email_body": body,
        "iteration": state.get("iteration", 0) + 1
    }


def review_agent(state: dict) -> dict:
    print("✅ Review Agent: Reviewing email...")

    prompt = f"""
    You are a senior sales manager and factuality reviewer.

    COMPANY:
    {state["company_name"]}

    VERIFIED COMPANY RESEARCH:
    {state["research"]}

    PAIN POINTS:
    {state["pain_points"]}

    GENERATED EMAIL:

    Subject:
    {state["email_subject"]}

    Email:
    {state["email_body"]}

    Review this email using these criteria:

    1. Personalization Score (1-10)
    2. Clarity Score (1-10)
    3. CTA Score (1-10)
    4. Factuality Score (1-10)
    5. Overall Score (1-10)

    ============================
    FACTUALITY CHECK
    ============================

    - Identify statistics that are not supported by the research.
    - Identify invented revenue, percentages, numbers, or growth claims.
    - Identify invented clients, case studies, or previous results.
    - Identify unsupported achievements or business facts.
    - Do not penalize reasonable business observations when they are
      clearly presented as possibilities.
    - If the email contains an unsupported factual claim,
      explicitly mention it in the feedback.

    IMPORTANT:
    - Do not invent information during your review.
    - Do not create fake evidence to justify a score.
    - Do NOT rewrite the email.

    Format EXACTLY:

    SCORES:
    Personalization: X/10
    Clarity: X/10
    CTA: X/10
    Factuality: X/10
    Overall: X/10

    FEEDBACK:
    [feedback here]
    """

    response = llm.invoke(prompt)

    clean = re.sub(
        r"<think>.*?</think>",
        "",
        response.content,
        flags=re.DOTALL
    ).strip()

    score_match = re.search(
        r"Overall:\s*(\d+)\s*/\s*10",
        clean,
        re.IGNORECASE
    )

    score = int(score_match.group(1)) if score_match else 0

    print("✅ Review complete!")

    return {
        "review": clean,
        "score": score,
        "email_subject": state["email_subject"],
        "email_body": state["email_body"]
    }