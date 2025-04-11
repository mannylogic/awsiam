# 🔐 AWS IAM Anomaly Detection & Automated Response Project

## 📌 Overview

Research shows that 1 in 4 people can still login to their account from previous jobs they left, granting them access to information they shouldn't have access to. This project demonstrates how to **detect and automatically respond to suspicious IAM activity in AWS**, leveraging native services like **Amazon GuardDuty**, **EventBridge**, **SNS**, **S3**, and **Lambda**. The solution is designed to identify potential threats — such as anomalous IAM logins or privilege escalation — and trigger automated security workflows.

---

## ⚙️ How It Works

1. **Amazon GuardDuty** continuously monitors AWS accounts for suspicious activity.
2. When an **IAM-related finding** is generated (e.g., `AnomalousBehavior`, `ConsoleLoginSuccess.B`), it is sent to **Amazon EventBridge**.
3. EventBridge filters for **specific finding types or severity** and triggers a **Lambda function**.
4. The Lambda function:
   - Parses the finding
   - Checks if the pattern matches an "interesting" or suspicious behavior
   - Sends a detailed alert to **SNS** (email, Slack, etc.)
   - Logs the incident to an **S3** bucket for further analysis, if needed
   - Initiates a response action to disable IAM user

---

## 🧠 Key Features

- ✅ **Event-driven detection** using GuardDuty + EventBridge  
- ✅ **Pattern-based filtering** on findings (e.g., privilege escalation, impossible travel)  
- ✅ **Severity threshold logic** (e.g., only act if severity ≥ 5)  
- ✅ **Notification and logging** via SNS and S3  
- ✅ **Modular, extensible Lambda** written in Python  

---

## 🛠️ Tools & Services Used

- AWS IAM  
- Amazon GuardDuty  
- AWS Lambda (Python 3.12)  
- Amazon EventBridge  
- Amazon SNS  
- Amazon S3  

---

## 🧪 Simulating Anomalies

To test the automation:
- Log in as a test IAM user from **different countries** using a VPN  
- Perform **unusual IAM actions** via AWS CLI or Console (e.g., attach admin policies, create users)  
- Wait for GuardDuty to detect and trigger the response workflow  

