{\rtf1\ansi\ansicpg1252\cocoartf2821
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Menlo-Regular;}
{\colortbl;\red255\green255\blue255;\red183\green111\blue179;\red24\green24\blue24;\red193\green193\blue193;
\red202\green202\blue202;\red194\green126\blue101;\red89\green138\blue67;\red70\green137\blue204;\red212\green214\blue154;
\red140\green211\blue254;\red167\green197\blue152;\red196\green83\blue86;\red205\green173\blue106;\red67\green192\blue160;
}
{\*\expandedcolortbl;;\cssrgb\c77255\c52549\c75294;\cssrgb\c12157\c12157\c12157;\cssrgb\c80000\c80000\c80000;
\cssrgb\c83137\c83137\c83137;\cssrgb\c80784\c56863\c47059;\cssrgb\c41569\c60000\c33333;\cssrgb\c33725\c61176\c83922;\cssrgb\c86275\c86275\c66667;
\cssrgb\c61176\c86275\c99608;\cssrgb\c70980\c80784\c65882;\cssrgb\c81961\c41176\c41176;\cssrgb\c84314\c72941\c49020;\cssrgb\c30588\c78824\c69020;
}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 import\cf4 \strokec4  boto3\cb1 \
\cf2 \cb3 \strokec2 import\cf4 \strokec4  json\cb1 \
\cf2 \cb3 \strokec2 import\cf4 \strokec4  re\cb1 \
\cf2 \cb3 \strokec2 from\cf4 \strokec4  datetime \cf2 \strokec2 import\cf4 \strokec4  datetime\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf4 \cb3 s3 \cf5 \strokec5 =\cf4 \strokec4  boto3.client(\cf6 \strokec6 's3'\cf4 \strokec4 )\cb1 \
\cb3 sns \cf5 \strokec5 =\cf4 \strokec4  boto3.client(\cf6 \strokec6 'sns'\cf4 \strokec4 )\cb1 \
\cb3 iam \cf5 \strokec5 =\cf4 \strokec4  boto3.client(\cf6 \strokec6 'iam'\cf4 \strokec4 )\cb1 \
\
\cb3 SNS_TOPIC_ARN \cf5 \strokec5 =\cf4 \strokec4  \cf6 \strokec6 'arn:aws:sns:eu-north-1:933822101455:testTopic'\cf4 \cb1 \strokec4 \
\cb3 S3_BUCKET_NAME \cf5 \strokec5 =\cf4 \strokec4  \cf6 \strokec6 'testbucketbabyyy'\cf4 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf7 \cb3 \strokec7 # Patterns i'm interested in\cf4 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3 INTERESTING_PATTERNS \cf5 \strokec5 =\cf4 \strokec4  [\cb1 \
\cb3     \cf6 \strokec6 "multiple countries"\cf4 \strokec4 ,\cb1 \
\cb3     \cf6 \strokec6 "suspicious api call"\cf4 \strokec4 ,\cb1 \
\cb3     \cf6 \strokec6 "credential exfiltration"\cf4 \strokec4 ,\cb1 \
\cb3     \cf6 \strokec6 "new geolocation"\cf4 \strokec4 ,\cb1 \
\cb3     \cf6 \strokec6 "unauthorized access"\cf4 \strokec4 ,\cb1 \
\cb3     \cf6 \strokec6 "impossible travel"\cf4 \cb1 \strokec4 \
\cb3 ]\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf8 \cb3 \strokec8 def\cf4 \strokec4  \cf9 \strokec9 lambda_handler\cf4 \strokec4 (\cf10 \strokec10 event\cf4 \strokec4 , \cf10 \strokec10 context\cf4 \strokec4 ):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     \cf9 \strokec9 print\cf4 \strokec4 (\cf6 \strokec6 "Received event:"\cf4 \strokec4 , json.dumps(event))\cb1 \
\cb3     detail \cf5 \strokec5 =\cf4 \strokec4  event[\cf6 \strokec6 'detail'\cf4 \strokec4 ]\cb1 \
\cb3     title \cf5 \strokec5 =\cf4 \strokec4  detail.get(\cf6 \strokec6 'title'\cf4 \strokec4 , \cf6 \strokec6 ''\cf4 \strokec4 ).lower()\cb1 \
\cb3     description \cf5 \strokec5 =\cf4 \strokec4  detail.get(\cf6 \strokec6 'description'\cf4 \strokec4 , \cf6 \strokec6 ''\cf4 \strokec4 ).lower()\cb1 \
\cb3     finding_type \cf5 \strokec5 =\cf4 \strokec4  detail.get(\cf6 \strokec6 'type'\cf4 \strokec4 , \cf6 \strokec6 ''\cf4 \strokec4 )\cb1 \
\cb3     severity \cf5 \strokec5 =\cf4 \strokec4  detail.get(\cf6 \strokec6 'severity'\cf4 \strokec4 , \cf11 \strokec11 0\cf4 \strokec4 )\cb1 \
\cb3     \cb1 \
\
\cb3 interesting_types \cf5 \strokec5 =\cf4 \strokec4  [\cb1 \
\cb3     \cf6 \strokec6 "IAMUser/AnomalousBehavior"\cf4 \strokec4 ,\cb1 \
\cb3     \cf6 \strokec6 "IAMUser/ConsoleLoginSuccess.B"\cf4 \cb1 \strokec4 \
\cb3 ]\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf4 \strokec4  \cf9 \strokec9 any\cf4 \strokec4 (t \cf2 \strokec2 in\cf4 \strokec4  finding_type \cf2 \strokec2 for\cf4 \strokec4  t \cf2 \strokec2 in\cf4 \strokec4  interesting_types) \cf8 \strokec8 and\cf4 \strokec4  (\cb1 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     severity \cf5 \strokec5 >=\cf4 \strokec4  \cf11 \strokec11 5\cf4 \strokec4  \cf8 \strokec8 or\cf4 \strokec4  \cb1 \
\cb3     \cf9 \strokec9 any\cf4 \strokec4 (keyword \cf2 \strokec2 in\cf4 \strokec4  title \cf2 \strokec2 or\cf4 \strokec4  keyword \cf2 \strokec2 in\cf4 \strokec4  description \cf2 \strokec2 for\cf4 \strokec4  keyword \cf2 \strokec2 in\cf4 \strokec4  INTERESTING_PATTERNS)\cb1 \
\cb3 ):\cb1 \
\cb3         \cf9 \strokec9 print\cf4 \strokec4 (\cf6 \strokec6 "Interesting IAM anomaly detected."\cf4 \strokec4 )\cb1 \
\
\cb3         user_name \cf5 \strokec5 =\cf4 \strokec4  extract_user_from_detail(detail)\cb1 \
\cb3         \cb1 \
\cb3         \cf2 \strokec2 if\cf4 \strokec4  user_name:\cb1 \
\cb3             disable_user(user_name)\cb1 \
\cb3         \cb1 \
\cb3         save_to_s3(detail)\cb1 \
\cb3         notify_sns(detail)\cb1 \
\cb3     \cf2 \strokec2 else\cf4 \strokec4 :\cb1 \
\cb3         \cf9 \strokec9 print\cf4 \strokec4 (\cf6 \strokec6 "Finding not considered critical. No action taken."\cf4 \strokec4 )\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf8 \cb3 \strokec8 def\cf4 \strokec4  \cf9 \strokec9 extract_user_from_detail\cf4 \strokec4 (\cf10 \strokec10 detail\cf4 \strokec4 ):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     \cf7 \strokec7 # Try to extract user from the resource\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 try\cf4 \strokec4 :\cb1 \
\cb3         user_arn \cf5 \strokec5 =\cf4 \strokec4  detail[\cf6 \strokec6 'resource'\cf4 \strokec4 ][\cf6 \strokec6 'resourceRole'\cf4 \strokec4 ]\cb1 \
\cb3         user_match \cf5 \strokec5 =\cf4 \strokec4  re.search(\cf8 \strokec8 r\cf12 \strokec12 'user\cf13 \strokec13 \\/\cf6 \strokec6 ([\cf12 \strokec12 \\w+=,.@-\cf6 \strokec6 ]\cf13 \strokec13 +\cf6 \strokec6 )\cf12 \strokec12 '\cf4 \strokec4 , user_arn)\cb1 \
\cb3         \cf2 \strokec2 if\cf4 \strokec4  user_match:\cb1 \
\cb3             \cf2 \strokec2 return\cf4 \strokec4  user_match.group(\cf11 \strokec11 1\cf4 \strokec4 )\cb1 \
\cb3     \cf2 \strokec2 except\cf4 \strokec4  \cf14 \strokec14 KeyError\cf4 \strokec4 :\cb1 \
\cb3         \cf2 \strokec2 pass\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 return\cf4 \strokec4  \cf8 \strokec8 None\cf4 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf8 \cb3 \strokec8 def\cf4 \strokec4  \cf9 \strokec9 disable_user\cf4 \strokec4 (\cf10 \strokec10 user_name\cf4 \strokec4 ):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     \cf2 \strokec2 try\cf4 \strokec4 :\cb1 \
\cb3         \cf9 \strokec9 print\cf4 \strokec4 (\cf8 \strokec8 f\cf6 \strokec6 "Disabling IAM user: \cf8 \strokec8 \{\cf4 \strokec4 user_name\cf8 \strokec8 \}\cf6 \strokec6 "\cf4 \strokec4 )\cb1 \
\cb3         iam.update_login_profile(\cf10 \strokec10 UserName\cf5 \strokec5 =\cf4 \strokec4 user_name, \cf10 \strokec10 PasswordResetRequired\cf5 \strokec5 =\cf8 \strokec8 True\cf4 \strokec4 )\cb1 \
\cb3         iam.delete_login_profile(\cf10 \strokec10 UserName\cf5 \strokec5 =\cf4 \strokec4 user_name)\cb1 \
\cb3         \cf9 \strokec9 print\cf4 \strokec4 (\cf8 \strokec8 f\cf6 \strokec6 "IAM user \cf8 \strokec8 \{\cf4 \strokec4 user_name\cf8 \strokec8 \}\cf6 \strokec6  login profile deleted."\cf4 \strokec4 )\cb1 \
\cb3     \cf2 \strokec2 except\cf4 \strokec4  \cf14 \strokec14 Exception\cf4 \strokec4  \cf2 \strokec2 as\cf4 \strokec4  e:\cb1 \
\cb3         \cf9 \strokec9 print\cf4 \strokec4 (\cf8 \strokec8 f\cf6 \strokec6 "Error disabling user \cf8 \strokec8 \{\cf4 \strokec4 user_name\cf8 \strokec8 \}\cf6 \strokec6 : \cf8 \strokec8 \{\cf4 \strokec4 e\cf8 \strokec8 \}\cf6 \strokec6 "\cf4 \strokec4 )\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf8 \cb3 \strokec8 def\cf4 \strokec4  \cf9 \strokec9 save_to_s3\cf4 \strokec4 (\cf10 \strokec10 finding\cf4 \strokec4 ):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     timestamp \cf5 \strokec5 =\cf4 \strokec4  datetime.utcnow().strftime(\cf6 \strokec6 '%Y-%m-\cf8 \strokec8 %d\cf6 \strokec6 T%H-%M-%SZ'\cf4 \strokec4 )\cb1 \
\cb3     key \cf5 \strokec5 =\cf4 \strokec4  \cf8 \strokec8 f\cf6 \strokec6 'guardduty-findings/\cf8 \strokec8 \{\cf4 \strokec4 timestamp\cf8 \strokec8 \}\cf6 \strokec6 .json'\cf4 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 try\cf4 \strokec4 :\cb1 \
\cb3         s3.put_object(\cb1 \
\cb3             \cf10 \strokec10 Bucket\cf5 \strokec5 =\cf4 \strokec4 S3_BUCKET_NAME,\cb1 \
\cb3             \cf10 \strokec10 Key\cf5 \strokec5 =\cf4 \strokec4 key,\cb1 \
\cb3             \cf10 \strokec10 Body\cf5 \strokec5 =\cf4 \strokec4 json.dumps(finding),\cb1 \
\cb3             \cf10 \strokec10 ContentType\cf5 \strokec5 =\cf6 \strokec6 'application/json'\cf4 \cb1 \strokec4 \
\cb3         )\cb1 \
\cb3         \cf9 \strokec9 print\cf4 \strokec4 (\cf8 \strokec8 f\cf6 \strokec6 "Finding saved to S3: s3://\cf8 \strokec8 \{\cf4 \strokec4 S3_BUCKET_NAME\cf8 \strokec8 \}\cf6 \strokec6 /\cf8 \strokec8 \{\cf4 \strokec4 key\cf8 \strokec8 \}\cf6 \strokec6 "\cf4 \strokec4 )\cb1 \
\cb3     \cf2 \strokec2 except\cf4 \strokec4  \cf14 \strokec14 Exception\cf4 \strokec4  \cf2 \strokec2 as\cf4 \strokec4  e:\cb1 \
\cb3         \cf9 \strokec9 print\cf4 \strokec4 (\cf8 \strokec8 f\cf6 \strokec6 "Error saving to S3: \cf8 \strokec8 \{\cf4 \strokec4 e\cf8 \strokec8 \}\cf6 \strokec6 "\cf4 \strokec4 )\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf8 \cb3 \strokec8 def\cf4 \strokec4  \cf9 \strokec9 notify_sns\cf4 \strokec4 (\cf10 \strokec10 finding\cf4 \strokec4 ):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf4 \cb3     \cf2 \strokec2 try\cf4 \strokec4 :\cb1 \
\cb3         sns.publish(\cb1 \
\cb3             \cf10 \strokec10 TopicArn\cf5 \strokec5 =\cf4 \strokec4 SNS_TOPIC_ARN,\cb1 \
\cb3             \cf10 \strokec10 Message\cf5 \strokec5 =\cf4 \strokec4 json.dumps(finding),\cb1 \
\cb3             \cf10 \strokec10 Subject\cf5 \strokec5 =\cf6 \strokec6 'GuardDuty Finding Alert'\cf4 \cb1 \strokec4 \
\cb3         )\cb1 \
\cb3         \cf9 \strokec9 print\cf4 \strokec4 (\cf6 \strokec6 "SNS notification sent."\cf4 \strokec4 )\cb1 \
\cb3     \cf2 \strokec2 except\cf4 \strokec4  \cf14 \strokec14 Exception\cf4 \strokec4  \cf2 \strokec2 as\cf4 \strokec4  e:\cb1 \
\cb3         \cf9 \strokec9 print\cf4 \strokec4 (\cf8 \strokec8 f\cf6 \strokec6 "Error sending SNS notification: \cf8 \strokec8 \{\cf4 \strokec4 e\cf8 \strokec8 \}\cf6 \strokec6 "\cf4 \strokec4 )\cb1 \
}