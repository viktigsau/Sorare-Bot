#!.venv/bin/python3

import requests
import bcrypt
from strat import turn


email = "viktigsau@gmail.com"
password = "VK8Pkf-e3y%*>aK"

salt_url = f"https://api.sorare.com/api/v1/users/{email}"

salt_response = requests.get(salt_url)

salt: str = salt_response.json()["salt"]

#print("salt:", salt)

hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')

#print("hashed_password:", hashed_password)

url = "https://api.sorare.com/graphql"

# GraphQL mutation for signing in
query = """
mutation SignInMutation($input: signInInput!) {
  signIn(input: $input) {
    currentUser {
      slug
    }
    jwtToken(aud: "myappname") {
      token
      expiredAt
    }
    errors {
      message
    }
  }
}
"""

# Variables for the query
variables = {
    "input": {
        "email": email,
        "password": hashed_password,
    }
}

# Prepare the request payload
payload = {
    "operationName": "SignInMutation",
    "query": query,
    "variables": variables,
}

# Step 3: Make the request to get the JWT token
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    data = response.json()
    if data["data"]["signIn"]["errors"] != []:
        print("Errors:", data["data"]["signIn"]["errors"])
    else:
        jwt_token = data["data"]["signIn"]["jwtToken"]["token"]
        expired_at = data["data"]["signIn"]["jwtToken"]["expiredAt"]
        print(f"Token expires At: {expired_at}")
else:
    print(f"Error: {response.status_code}, {response.text}")

