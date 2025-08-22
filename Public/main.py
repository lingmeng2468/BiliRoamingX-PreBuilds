import os
import requests

Github_Token = os.environ["PAT"]
Folder_Path = os.environ["Folder_Path"]

temurin_version_url = "https://api.adoptium.net/v3/info/available_releases"
temurin_version_headers = {
    "User-Agent": "Github Actions"
}

temurin_version_response = requests.request("GET", temurin_version_url, headers=temurin_version_headers)
print(f"Temurin Version Response Status Code: {temurin_version_response.status_code}")
print(f"Temurin Version Response Text: {temurin_version_response.text}")

temurin_version_data = temurin_version_response.json()

Github_ENV = os.getenv('GITHUB_ENV')
with open(Github_ENV, "a") as Github_ENV_File:
    Github_ENV_File.write("Temurin_Version=" + str(temurin_version_data["most_recent_feature_release"]))

uber_apk_signer_url = "https://api.github.com/repos/patrickfav/uber-apk-signer/releases/latest"
uber_apk_signer_payload = {}
uber_apk_signer_headers = {
    'Authorization': 'Bearer ' + Github_Token
}

uber_apk_signer_response = requests.request("GET", uber_apk_signer_url, headers=uber_apk_signer_headers, data=uber_apk_signer_payload)
print(f"Uber APK Signer Response Status Code: {uber_apk_signer_response.status_code}")
print(f"Uber APK Signer Response Text: {uber_apk_signer_response.text}")

uber_apk_signer_data = uber_apk_signer_response.json()

uber_apk_signer_jar_url = ""
if isinstance(uber_apk_signer_data, dict) and 'assets' in uber_apk_signer_data:
    for asset in uber_apk_signer_data['assets']:
        if asset['name'].endswith('.jar') and not uber_apk_signer_jar_url:
            uber_apk_signer_jar_url = asset['browser_download_url']
        if uber_apk_signer_jar_url:
            break

if uber_apk_signer_jar_url:
    uber_apk_signer_jar_response = requests.request("GET", uber_apk_signer_jar_url)
    with open(Folder_Path + "uber-apk-signer.jar", "wb") as f:
        f.write(uber_apk_signer_jar_response.content)
else:
    print("Failed to find uber-apk-signer.jar URL")