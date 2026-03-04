import os
import time
from playwright.sync_api import sync_playwright

def authenticate_and_add_emails(competition_slug: str, emails: list[str], user_data_dir: str = "./kaggle_chrome_profile"):
    """
    Automates the addition of emails to a Kaggle private competition using a 
    persistent browser session to bypass Google OAuth bot detection.
    """
    # Ensure the local directory exists to store session cookies and local storage
    os.makedirs(user_data_dir, exist_ok=True)

    with sync_playwright() as p:
        # Launch a persistent context using the local Chrome installation
        print("Initializing persistent browser context...")
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False, # Must remain False to pass initial bot heuristics
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        # Use the default page created by the persistent context
        page = context.pages[0] if context.pages else context.new_page()

        # --- State 1: Authentication Validation ---
        page.goto("https://www.kaggle.com/")
        print("Checking authentication state...")
        print("If a login screen appears, please sign in manually with Google.")
        print("The script will wait up to 2 minutes for you to complete this.")
        
        # Block execution until the browser lands on the authenticated homepage
        # On subsequent runs, this resolves in O(1) time as cookies are loaded from disk.
        page.wait_for_url("https://www.kaggle.com/", timeout=120000)
        print("Authentication confirmed.")

        # --- State 2: Navigate to Host Settings ---
        settings_url = f"https://www.kaggle.com/c/{competition_slug}/host/settings"
        print(f"Navigating to {settings_url}...")
        page.goto(settings_url)

        # Wait for the main settings DOM to settle
        page.wait_for_selector("text='Privacy, Access & Resources'", timeout=15000)

        # --- State 3: Trigger the Sidebar ---
        print("Locating 'Manage Email List' button...")
        manage_button = page.locator("button:has-text('Manage Email List')")
        manage_button.wait_for(state="visible", timeout=15000)
        manage_button.click()

        print("Waiting for sidebar DOM to mount...")
        # Target the input field inside the sidebar
        email_input = page.locator("input[placeholder*='email' i]") 
        email_input.wait_for(state="visible", timeout=10000)

        # Target the add/save button. Adjust text if Kaggle uses 'Add', 'Save', or 'Invite'
        add_button = page.locator("button:has-text('Add')") 

        # --- State 4: The Injection Loop ---
        print(f"Starting injection loop for {len(emails)} emails...")
        for email in emails:
            print(f" -> Injecting: {email}")
            
            # Fill the input field
            email_input.fill(email)
            
            # Try clicking the Add button; if it's not a discrete button, 
            # fall back to pressing Enter to tokenize the email input.
            if add_button.is_visible():
                add_button.click()
            else:
                page.keyboard.press("Enter")
            
            # Artificial delay to prevent application-layer rate limiting
            time.sleep(1.5) 

        # --- State 5: Commit and Cleanup ---
        # If there is a final save button to commit the list to the server, click it
        save_button = page.locator("button:has-text('Save')")
        if save_button.is_visible():
            print("Committing final list to Kaggle...")
            save_button.click()
            save_button.wait_for(state="hidden", timeout=10000) 

        print("Execution complete. Closing browser.")
        context.close()

if __name__ == "__main__":
    # Define your competition slug (the part of the URL after /c/)
    TARGET_COMPETITION = "my-private-competition-slug"
    
    # Define the list of emails to authorize
    TARGET_EMAILS = [
        "student1@university.edu",
        "student2@university.edu",
        "researcher@lab.org"
    ]

    # Execute the workflow
    authenticate_and_add_emails(TARGET_COMPETITION, TARGET_EMAILS)
