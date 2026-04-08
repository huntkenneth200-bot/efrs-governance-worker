import { SQSClient, SendMessageCommand } from "@aws-sdk/client-sqs";

const client = new SQSClient({ region: "us-east-2" });

const params = {
  QueueUrl: process.env.QUEUE_URL,
  MessageBody: JSON.stringify({ test: "Hello from IdeaPad" }),
};

const run = async () => {
  try {
    const data = await client.send(new SendMessageCommand(params));
    console.log("Message sent:", data);
  } catch (err) {
    console.error("Error sending message:", err);
  }
};

run();
