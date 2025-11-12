import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Button } from '../ui/button';
import { Textarea } from '../ui/textarea';
import { Label } from '../ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Alert, AlertDescription } from '../ui/alert';
import { Progress } from '../ui/progress';
import { Badge } from '../ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Upload, Code2, AlertCircle, CheckCircle2, Loader2, TrendingUp, Shield, Zap } from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

const LANGUAGES = [
  'python', 'javascript', 'typescript', 'java', 'cpp', 'c', 'csharp',
  'go', 'rust', 'php', 'ruby', 'swift', 'kotlin', 'scala', 'r', 'sql'
];

export default function AdvancedCodeAnalyzer() {
  const { token } = useAuth();
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [isDragging, setIsDragging] = useState(false);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = async (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      setFile(droppedFile);
      const reader = new FileReader();
      reader.onload = (event) => {
        setCode(event.target.result);
      };
      reader.readAsText(droppedFile);
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      // Read file content
      const reader = new FileReader();
      reader.onload = (event) => {
        setCode(event.target.result);
      };
      reader.readAsText(selectedFile);
    }
  };

  const handleAnalyze = async () => {
    if (!code.trim()) {
      setError('Please enter code or upload a file');
      return;
    }

    setError('');
    setLoading(true);
    setResult(null);

    try {
      const formData = new FormData();
      if (file) {
        formData.append('file', file);
      } else {
        formData.append('code', code);
      }
      formData.append('language', language);

      const headers = token
        ? { Authorization: `Bearer ${token}` }
        : {};

      const response = await axios.post(
        `${API_BASE_URL}/api/v3/code/analyze`,
        formData,
        { headers }
      );

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getSeverityColor = (severity) => {
    if (severity === 'high') return 'destructive';
    if (severity === 'medium') return 'default';
    return 'secondary';
  };

  return (
    <div className="container py-8 space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Advanced Code Analyzer</h1>
        <p className="text-muted-foreground mt-2">
          Get quality scoring, error detection, and optimization suggestions
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Upload or Paste Code</CardTitle>
          <CardDescription>
            Supports 18 programming languages
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>Programming Language</Label>
            <Select value={language} onValueChange={setLanguage}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {LANGUAGES.map((lang) => (
                  <SelectItem key={lang} value={lang}>
                    {lang.charAt(0).toUpperCase() + lang.slice(1)}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label>Upload File</Label>
            <div
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              className={`border-2 border-dashed rounded-lg p-6 transition-colors ${
                isDragging ? 'border-primary bg-primary/10' : 'border-muted'
              }`}
            >
              <div className="text-center">
                <Upload className="h-10 w-10 mx-auto mb-3 text-muted-foreground" />
                <p className="text-sm text-muted-foreground mb-2">
                  {file ? file.name : 'Drag and drop your code file here'}
                </p>
                <p className="text-xs text-muted-foreground mb-3">or</p>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => document.getElementById('file-input').click()}
                >
                  Choose File
                </Button>
                <input
                  id="file-input"
                  type="file"
                  accept=".py,.js,.ts,.java,.cpp,.c,.cs,.go,.rs,.php,.rb,.swift,.kt,.scala,.r,.sql"
                  onChange={handleFileChange}
                  className="hidden"
                />
              </div>
            </div>
          </div>

          <div className="space-y-2">
            <Label>Or Paste Code</Label>
            <Textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="Paste your code here..."
              className="font-mono text-sm min-h-[200px]"
            />
          </div>

          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <Button
            onClick={handleAnalyze}
            disabled={loading || !code.trim()}
            className="w-full"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Code2 className="mr-2 h-4 w-4" />
                Analyze Code
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {result && (
        <div className="space-y-6">
          {/* Quality Score */}
          <Card>
            <CardHeader>
              <CardTitle>Quality Score</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-4xl font-bold">
                    <span className={getScoreColor(result.quality_score)}>
                      {result.quality_score}
                    </span>
                    <span className="text-muted-foreground">/100</span>
                  </span>
                  <Badge variant={result.has_errors ? 'destructive' : 'default'}>
                    {result.error_count} {result.error_count === 1 ? 'issue' : 'issues'}
                  </Badge>
                </div>

                <div className="space-y-2">
                  {Object.entries(result.score_breakdown).map(([category, score]) => (
                    <div key={category}>
                      <div className="flex justify-between text-sm mb-1">
                        <span className="capitalize">{category}</span>
                        <span>{score}/20</span>
                      </div>
                      <Progress value={(score / 20) * 100} />
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Detailed Results */}
          <Card>
            <CardContent className="pt-6">
              <Tabs defaultValue="errors">
                <TabsList className="w-full">
                  <TabsTrigger value="errors" className="flex-1">
                    Errors ({result.errors.length})
                  </TabsTrigger>
                  <TabsTrigger value="corrections" className="flex-1">
                    Corrections ({result.line_corrections.length})
                  </TabsTrigger>
                  <TabsTrigger value="suggestions" className="flex-1">
                    Tips
                  </TabsTrigger>
                </TabsList>

                <TabsContent value="errors" className="space-y-3 mt-4">
                  {result.errors.length > 0 ? (
                    result.errors.map((error, idx) => (
                      <div key={idx} className="p-4 border rounded-lg">
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex items-center gap-2">
                            <AlertCircle className="h-4 w-4 text-destructive" />
                            <span className="font-medium capitalize">{error.type.replace('_', ' ')}</span>
                          </div>
                          <Badge variant={getSeverityColor(error.severity)}>
                            {error.severity}
                          </Badge>
                        </div>
                        {error.line && (
                          <div className="text-sm text-muted-foreground mb-1">
                            Line {error.line}{error.column && `, Column ${error.column}`}
                          </div>
                        )}
                        <div className="text-sm">{error.message}</div>
                        {error.suggestion && (
                          <div className="mt-2 text-sm text-green-600">
                            💡 {error.suggestion}
                          </div>
                        )}
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-8 text-muted-foreground">
                      <CheckCircle2 className="h-12 w-12 mx-auto mb-2 text-green-500" />
                      No errors found! Great job! 🎉
                    </div>
                  )}
                </TabsContent>

                <TabsContent value="corrections" className="space-y-3 mt-4">
                  {result.line_corrections.length > 0 ? (
                    result.line_corrections.map((correction, idx) => (
                      <div key={idx} className="p-4 border rounded-lg space-y-2">
                        <div className="text-sm font-medium">Line {correction.line}</div>
                        <div className="space-y-1">
                          <div className="text-sm">
                            <span className="text-red-600">- </span>
                            <code className="bg-red-50 px-1 py-0.5 rounded">{correction.original}</code>
                          </div>
                          <div className="text-sm">
                            <span className="text-green-600">+ </span>
                            <code className="bg-green-50 px-1 py-0.5 rounded">{correction.corrected}</code>
                          </div>
                        </div>
                        <div className="text-sm text-muted-foreground">
                          {correction.reason}
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-8 text-muted-foreground">
                      No corrections needed
                    </div>
                  )}
                </TabsContent>

                <TabsContent value="suggestions" className="space-y-4 mt-4">
                  {result.performance_tips.length > 0 && (
                    <div>
                      <h4 className="font-medium mb-2 flex items-center gap-2">
                        <Zap className="h-4 w-4 text-yellow-500" />
                        Performance Tips
                      </h4>
                      <ul className="space-y-2">
                        {result.performance_tips.map((tip, idx) => (
                          <li key={idx} className="text-sm p-2 bg-yellow-50 dark:bg-yellow-950 rounded">
                            {tip}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {result.security_issues.length > 0 && (
                    <div>
                      <h4 className="font-medium mb-2 flex items-center gap-2">
                        <Shield className="h-4 w-4 text-red-500" />
                        Security Issues
                      </h4>
                      <ul className="space-y-2">
                        {result.security_issues.map((issue, idx) => (
                          <li key={idx} className="text-sm p-2 bg-red-50 dark:bg-red-950 rounded">
                            {issue}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {result.suggestions.length > 0 && (
                    <div>
                      <h4 className="font-medium mb-2 flex items-center gap-2">
                        <TrendingUp className="h-4 w-4 text-blue-500" />
                        General Suggestions
                      </h4>
                      <ul className="space-y-2">
                        {result.suggestions.map((suggestion, idx) => (
                          <li key={idx} className="text-sm p-2 bg-blue-50 dark:bg-blue-950 rounded">
                            {suggestion}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>

          {/* Corrected Code */}
          {result.corrected_code && (
            <Card>
              <CardHeader>
                <CardTitle>Corrected Code</CardTitle>
              </CardHeader>
              <CardContent>
                <pre className="bg-muted p-4 rounded-lg overflow-x-auto text-sm">
                  <code>{result.corrected_code}</code>
                </pre>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
