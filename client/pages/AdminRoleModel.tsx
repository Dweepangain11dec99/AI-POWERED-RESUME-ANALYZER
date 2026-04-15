import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function AdminRoleModel() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<any>(null);
  const [message, setMessage] = useState<string | null>(null);

  const basicHeader = () => {
    const token = btoa(`${username}:${password}`);
    return { 'Authorization': `Basic ${token}` };
  };

  const fetchStatus = async () => {
    setLoading(true);
    setMessage(null);
    try {
      const res = await fetch(`${API_URL}/admin/role-predictor/status`, {
        method: 'GET',
        headers: {
          ...basicHeader(),
          'Content-Type': 'application/json'
        }
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `HTTP ${res.status}`);
      }
      const data = await res.json();
      setStatus(data);
      setMessage('Status fetched');
    } catch (err: any) {
      setMessage(`Error: ${err.message}`);
      setStatus(null);
    } finally {
      setLoading(false);
    }
  };

  const retrain = async () => {
    setLoading(true);
    setMessage(null);
    try {
      const formData = new FormData();
      if (file) formData.append('file', file);
      const res = await fetch(`${API_URL}/admin/role-predictor/retrain`, {
        method: 'POST',
        body: formData,
        headers: {
          ...basicHeader()
        }
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `HTTP ${res.status}`);
      }
      const data = await res.json();
      setMessage('Retrain succeeded');
      setStatus({ trained: data.trained, saved: data.saved });
    } catch (err: any) {
      setMessage(`Retrain failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6">
      <div className="max-w-3xl mx-auto space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Admin — Role Predictor</CardTitle>
            <CardDescription>Retrain the role predictor and check model status (HTTP Basic auth)</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label>Username</Label>
                <Input value={username} onChange={(e) => setUsername((e.target as any).value)} />
              </div>
              <div>
                <Label>Password</Label>
                <Input type="password" value={password} onChange={(e) => setPassword((e.target as any).value)} />
              </div>
            </div>

            <div>
              <Label>Training CSV (optional)</Label>
              <Input type="file" accept=".csv" onChange={(e) => setFile((e.target as any).files?.[0] || null)} />
            </div>

            <div className="flex items-center gap-3">
              <Button onClick={fetchStatus} disabled={loading || !username || !password}>Check Status</Button>
              <Button onClick={retrain} disabled={loading || !username || !password}>Retrain</Button>
            </div>

            {message && <div className="text-sm text-muted-foreground">{message}</div>}

            {status && (
              <div className="mt-4">
                <div>Trained: {String(status.trained)}</div>
                {status.saved !== undefined && <div>Saved: {String(status.saved)}</div>}
              </div>
            )}
          </CardContent>
        </Card>

      </div>
    </div>
  );
}
