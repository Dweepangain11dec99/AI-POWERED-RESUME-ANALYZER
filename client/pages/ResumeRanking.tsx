import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function ResumeRanking() {
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any[]>([]);

  const handleRank = async () => {
    if (!jobDescription) return;
    setLoading(true);
    try {
      const form = new FormData();
      form.append('job_description', jobDescription);
      form.append('top_k', '10');
      const res = await fetch(`${API_URL}/resume/rank`, {
        method: 'POST',
        body: form,
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        }
      });
      const data = await res.json();
      setResults(data.ranked || []);
    } catch (err) {
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6">
      <div className="max-w-3xl mx-auto">
        <Card>
          <CardHeader>
            <CardTitle>Resume Ranking</CardTitle>
            <CardDescription>Rank stored resumes for a given job description</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Textarea placeholder="Paste job description here..." value={jobDescription} onChange={(e) => setJobDescription((e.target as any).value)} className="min-h-[200px]" />
            <div className="flex gap-3">
              <Button onClick={handleRank} disabled={loading || !jobDescription}>Rank Resumes</Button>
            </div>

            <div className="mt-4">
              {results.map((r, idx) => (
                <div key={idx} className="p-3 border rounded mb-2">
                  <div className="font-medium">Resume ID: {r.resume_id} — Score: {(r.score * 100).toFixed(1)}%</div>
                  <div className="text-sm text-muted-foreground">Skills: {(r.skills || []).slice(0,5).join(', ')}</div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
