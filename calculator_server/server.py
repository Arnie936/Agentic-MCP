from mcp.server.fastmcp import FastMCP
import httpx

# Initialize FastMCP server
mcp = FastMCP("calculator")

# Constants
SUPPORT_PLAYBOOK = """# Customer Support Playbook  
Version: 1.4  
Last Updated: 2025-12-08  

## 1. Company Overview
We provide digital services, AI automation solutions and online education.  
Core values: **clarity, speed, transparency, helpfulness**.

---

## 2. Tone & Communication Rules
Always:
- Use clear, friendly language  
- Offer short answers before long explanations  
- Provide step-by-step solutions  
- Confirm understanding (“Does this solve your issue?”)

Never:
- Blame the user  
- Make technical claims without certainty  
- Promise features that don't exist  

---

## 3. Product Overview
### **Product A: AI Automation Suite**
A no-code/low-code platform for building automation workflows with:
- API integrations  
- AI agents  
- Database connections  
- Real-time triggers  

Key benefits:
- Saves time  
- Reduces manual work  
- Works with any business size  

---

## 4. Supported Workflows (Common Solutions)
### 4.1 Resetting User Password
Steps:
1. Go to **Account Settings → Security**  
2. Click **Reset Password**  
3. Email confirmation is required  
4. If email doesn’t arrive:  
   - Check spam  
   - Request a resend  
   - Confirm correct email on file  

---

### 4.2 Troubleshooting Login Issues
Possible causes:
- Wrong password  
- Browser cache  
- Cookies blocked  
- Outdated browser  

Fix:
1. Clear cache  
2. Try private mode  
3. Reset password  
4. If still failing → escalate with screenshot + timestamp  

---

## 5. Refund Policy (Public)
Refunds allowed within **30 days** of purchase if:
- The product does not work as described  
- The customer has attempted at least one troubleshooting step  

Refunds *not* issued when:
- The customer "changed their mind"  
- The purchase was made more than 30 days ago  

---

## 6. Escalation Rules
A ticket must be escalated if:
- The customer is stuck after 2 troubleshooting rounds  
- There is a billing or legal issue  
- There is a potential data leak or privacy concern  

Escalation targets:
- Technical issues → Tech Team  
- Billing issues → Finance  
- Abuse or harassment → Legal  

---

## 7. Common Templates

### 7.1 “Issue Received” Template
"""

WEBINAR_PROMPT = """# Webinar to Blog Post Template

You are a content specialist tasked with converting a webinar transcript into an engaging blog post. Maintain the educational value while making the content more readable and web-friendly.

Webinar Information:
Title: {webinar_title}
Date: {webinar_date}
Speakers: {speakers}

Transcript:
{transcript}

Please convert this webinar into a blog post using the following structure:

## Title [Create an engaging blog title]

## Introduction
- Hook the reader's attention
- Provide context about the webinar
- Preview the key takeaways

## Main Content
Divide the content into 3-5 main sections, each with:
- Clear subheadings
- Key points from the webinar
- Supporting examples or case studies
- Expert quotes from speakers

## Key Takeaways
- List 3-5 main lessons or insights
- Include actionable tips
- Highlight unique perspectives

## Conclusion
- Summarize the main points
- Call to action
- Additional resources

Formatting Guidelines:
- Use short paragraphs
- Include bullet points for lists
- Break up text with subheadings
- Incorporate speaker quotes
- Add transition sentences between sections"""

@mcp.resource("support://playbook")
def get_playbook() -> str:
    """Get the customer support playbook"""
    return SUPPORT_PLAYBOOK

@mcp.prompt()
def webinar_to_blog(webinar_title: str, webinar_date: str, speakers: str, transcript: str) -> str:
    """Convert a webinar transcript into a blog post"""
    return WEBINAR_PROMPT.format(
        webinar_title=webinar_title,
        webinar_date=webinar_date,
        speakers=speakers,
        transcript=transcript
    )

@mcp.tool()
async def send_to_webhook(prompt: str) -> str:
    """Send a prompt to the n8n webhook and get the response.

    Args:
        prompt: The text prompt to process
    """
    webhook_url = "Your_URL"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(webhook_url, json={"prompt": prompt}, timeout=30.0)
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as e:
            return f"Error sending request: {str(e)}"

@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b

@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract b from a"""
    return a - b

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

