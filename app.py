import streamlit as st
import requests
import json

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = "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"
REPO_OWNER = "Sachin-B-A"
REPO_NAME = "Testing_Github_Integration"

st.title('GitHub Integration Test Interface')

st.markdown("""
Welcome to the **GitHub Integration Test Interface**. This tool allows you to interact with GitHub repositories by:

- **Creating issues** to track tasks or bugs.
- **Updating existing issues** with new details.
- **Assigning roles** to collaborators in your repository.

Use this interface to test GitHub integrations seamlessly.
""")

st.sidebar.title("Navigation")

action = st.sidebar.radio(
    "Select an Action:",
    ["Create Issue", "Update Task", "Assign Role"],
    index=0
)

if "log" not in st.session_state:
    st.session_state["log"] = []

def create_github_issue(title, body):
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {
        "title": title,
        "body": body
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        return "Issue created successfully!"
    else:
        return f"Failed to create issue: {response.status_code} - {response.text}"

def update_github_issue(issue_number, title=None, body=None):
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue_number}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {}
    if title:
        data["title"] = title
    if body:
        data["body"] = body
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return f"Issue #{issue_number} updated successfully!"
    else:
        return f"Failed to update issue: {response.status_code} - {response.text}"

def assign_role_to_user(username, role):
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/collaborators/{username}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {"permission": role}
    response = requests.put(url, headers=headers, data=json.dumps(data))
    if response.status_code == 204:
        return f"Role '{role}' assigned to {username}."
    else:
        return f"Failed to assign role: {response.status_code} - {response.text}"

if action == "Create Issue":
    st.header("Create a New GitHub Issue")
    st.write("Provide details to create a new issue in the repository.")
    issue_title = st.text_input("Issue Title", placeholder="Enter the issue title here")
    issue_body = st.text_area("Issue Description", placeholder="Describe the issue in detail")
    if st.button("Create Issue"):
        if issue_title and issue_body:
            result = create_github_issue(issue_title, issue_body)
            st.session_state["log"].append(result)
            st.success(result)
        else:
            st.error("Please fill in both the title and description.")

elif action == "Update Task":
    st.header("Update an Existing GitHub Issue")
    st.write("Provide the issue number and the new details to update.")
    issue_number = st.number_input("Issue Number", min_value=1, step=1, help="Enter the ID of the issue to update")
    new_title = st.text_input("New Title (Optional)", placeholder="Enter a new title for the issue")
    new_body = st.text_area("New Description (Optional)", placeholder="Update the issue description")
    if st.button("Update Task"):
        if issue_number:
            result = update_github_issue(issue_number, new_title, new_body)
            st.session_state["log"].append(result)
            st.success(result)
        else:
            st.error("Please enter a valid issue number.")

elif action == "Assign Role":
    st.header("Assign a Role to a GitHub User")
    st.write("Provide the username and select the role to assign.")
    username = st.text_input("GitHub Username", placeholder="Enter the GitHub username")
    role = st.selectbox("Select Role", ["pull", "push", "admin"], help="Choose the permission level for the user")
    if st.button("Assign Role"):
        if username:
            result = assign_role_to_user(username, role)
            st.session_state["log"].append(result)
            st.success(result)
        else:
            st.error("Please enter a GitHub username.")

st.sidebar.subheader("Operation Logs")

with st.sidebar.expander("View Operation Logs"):
    for i, log_entry in enumerate(st.session_state["log"], start=1):
        st.markdown(
            f"""<div style='border: 1px solid #28a745; background-color: #32CD32; padding: 10px; margin-bottom: 10px; border-radius: 5px; color: white;'>
            <strong>Log {i}:</strong> {log_entry}
            </div>""",
            unsafe_allow_html=True
        )


st.markdown("""
---
### About
This tool was built to facilitate GitHub API testing for common repository management tasks. 
Enjoy exploring the functionalities and improving your workflows!
""")
