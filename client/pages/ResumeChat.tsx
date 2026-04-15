import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function ResumeChat() {
  const [resumeId, setResumeId] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState('');

  const handleAsk = async () => {
    if (!resumeId || !message) return;
    setLoading(true);
    try {
      const form = new FormData();
      form.append('resume_id', resumeId);
      form.append('message', message);
      const res = await fetch(`${API_URL}/resume/chat`, {
        method: 'POST',
        body: form,
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        }
      });
      const data = await res.json();
      setAnswer(data.answer || 'No answer');
    } catch (err) {
      setAnswer('Failed to get answer');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6">
      <div className="max-w-2xl mx-auto">
        <Card>
          <CardHeader>
            <CardTitle>Resume Chat</CardTitle>
            <CardDescription>Ask questions about a stored resume</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Input placeholder="Resume ID" value={resumeId} onChange={(e) => setResumeId((e.target as any).value)} />
            </div>
            <div>
              <Textarea placeholder="Ask something about the resume..." value={message} onChange={(e) => setMessage((e.target as any).value)} />
            </div>
            <div className="flex gap-3">
              <Button onClick={handleAsk} disabled={loading || !resumeId || !message}>Ask</Button>
            </div>
            {answer && (
              <div className="mt-4 p-4 bg-muted rounded">
                <div className="font-medium mb-2">Answer</div>
                <div>{answer}</div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
