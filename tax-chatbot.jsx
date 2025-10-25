import { useState } from "react";
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";

export default function TaxChatbot() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hello! I can help you calculate your tax. What's your annual income?" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [context, setContext] = useState({ income: null, country: null });

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages(newMessages);
    setLoading(true);

    try {
      let reply = "";

      // Step 1: Capture income
      if (!context.income) {
        const income = parseFloat(input);
        if (isNaN(income) || income <= 0) {
          reply = "Please enter a valid income amount (a number greater than 0).";
        } else {
          setContext({ ...context, income });
          reply = "Got it! Now, please tell me your country (e.g., US, UK, NG, CA).";
        }
      }
      // Step 2: Capture country and calculate tax via text-based API
      else if (!context.country) {
        const country = input.trim().toLowerCase();
        setContext({ ...context, country });

        const response = await fetch(`${process.env.REACT_APP_TAX_API_URL || "https://api.example.com/tax/calculate"}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ income: context.income, country }),
        });

        if (!response.ok) throw new Error("Failed to fetch tax data");

        // Handle both text and JSON responses gracefully
        const text = await response.text();
        let parsedText = text;

        try {
          const data = JSON.parse(text);
          if (data.taxAmount && data.classification) {
            parsedText = `Your estimated tax is $${data.taxAmount}. Classification: ${data.classification}. Would you like to calculate again?`;
          }
        } catch {
          // if plain text, keep as is
        }

        reply = parsedText;
        setContext({ income: null, country: null });
      } else {
        reply = "Let's start again. What's your annual income?";
        setContext({ income: null, country: null });
      }

      setMessages((prev) => [...prev, { sender: "bot", text: reply }]);
    } catch (err) {
      setMessages((prev) => [...prev, { sender: "bot", text: "Error: " + err.message }]);
    } finally {
      setInput("");
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-50 p-4">
      <Card className="w-full max-w-md shadow-lg flex flex-col">
        <CardHeader>
          <h2 className="text-xl font-semibold text-center">Tax Chatbot</h2>
        </CardHeader>
        <CardContent className="flex flex-col h-[500px] overflow-hidden">
          <div className="flex-1 overflow-y-auto mb-3 space-y-3 p-2 bg-gray-100 rounded-md">
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`p-2 rounded-lg max-w-[80%] ${
                  msg.sender === "bot"
                    ? "bg-blue-100 text-gray-800 self-start"
                    : "bg-green-100 text-gray-900 self-end ml-auto"
                }`}
              >
                {msg.text}
              </div>
            ))}
            {loading && (
              <div className="flex items-center space-x-2 text-gray-500">
                <Loader2 className="animate-spin" />
                <span>Thinking...</span>
              </div>
            )}
          </div>
          <form onSubmit={handleSend} className="flex space-x-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              disabled={loading}
            />
            <Button type="submit" disabled={loading}>
              Send
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}