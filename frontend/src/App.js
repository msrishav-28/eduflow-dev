import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, NavLink, useNavigate } from "react-router-dom";
import { NavigationMenu, NavigationMenuList, NavigationMenuItem } from "./components/ui/navigation-menu";
import { Button } from "./components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "./components/ui/card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "./components/ui/tabs";
import { Textarea } from "./components/ui/textarea";
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from "./components/ui/accordion";
import { Label } from "./components/ui/label";
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "./components/ui/select";
// (theme icon button implemented below; no Switch component)
import { motion, useMotionValue, useSpring } from "framer-motion";
import { Sparkles, MessageSquare, FileText, ListChecks, Code2, ArrowRight, BookOpen, Play, Sun, Moon, Loader2 } from "lucide-react";
import axios from "axios";

// V3 Components
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import LoginForm from "./components/auth/LoginForm";
import SignupForm from "./components/auth/SignupForm";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import Dashboard from "./components/dashboard/Dashboard";
import AdvancedCodeAnalyzer from "./components/code/AdvancedCodeAnalyzer";
import UserMenu from "./components/common/UserMenu";
import ProfilePage from "./components/profile/ProfilePage";

// API client
const API_BASE_URL = "http://localhost:8000/api";
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

// THEME TOGGLE (light/dark using CSS class on <html>)
function useThemeMode() {
  const [mode, setMode] = React.useState(() => {
    const saved = typeof window !== "undefined" ? localStorage.getItem("flow_theme") : null;
    return saved || "dark"; // default dark
  });

  React.useEffect(() => {
    const el = document.documentElement;
    el.classList.remove("theme-light", "theme-dark");
    el.classList.add(mode === "dark" ? "theme-dark" : "theme-light");
    localStorage.setItem("flow_theme", mode);
  }, [mode]);

  return { mode, setMode };
}

function ThemeToggle() {
  const { mode, setMode } = useThemeMode();
  const isDark = mode === "dark";
  return (
    <button
      aria-label={isDark ? "Switch to light mode" : "Switch to dark mode"}
      className="theme-icon-btn"
      onClick={() => setMode(isDark ? "light" : "dark")}
      title={isDark ? "Switch to light mode" : "Switch to dark mode"}
    >
      {isDark ? <Sun size={18} /> : <Moon size={18} />}
    </button>
  );
}

function Header() {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  React.useEffect(() => {
    const onScroll = () => {
      const h = document.querySelector('.site-header');
      if (!h) return;
      if (window.scrollY > 8) h.classList.add('scrolled');
      else h.classList.remove('scrolled');
    };
    window.addEventListener('scroll', onScroll);
    onScroll();
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <header className="site-header">
      <div className="container header-wrap">
        <NavLink to="/" className="brand" aria-label="AI Study Platform Home">
          <div className="brand-mark" />
          <span className="brand-text">EduFlow</span>
        </NavLink>

        <nav className="main-nav">
          <NavigationMenu>
            <NavigationMenuList>
              <NavigationMenuItem>
                <NavLink to="/qa" className="nav-link">Q&amp;A</NavLink>
              </NavigationMenuItem>
              <NavigationMenuItem>
                <NavLink to="/summarizer" className="nav-link">Summarizer</NavLink>
              </NavigationMenuItem>
              <NavigationMenuItem>
                <NavLink to="/mcq" className="nav-link">MCQ Generator</NavLink>
              </NavigationMenuItem>
              <NavigationMenuItem>
                <NavLink to="/code-explainer" className="nav-link">Code Explainer</NavLink>
              </NavigationMenuItem>
              {isAuthenticated && (
                <>
                  <NavigationMenuItem>
                    <NavLink to="/code-analyzer" className="nav-link">Code Analyzer</NavLink>
                  </NavigationMenuItem>
                  <NavigationMenuItem>
                    <NavLink to="/dashboard" className="nav-link">Dashboard</NavLink>
                  </NavigationMenuItem>
                </>
              )}
              <NavigationMenuItem>
                <NavLink to="/about" className="nav-link">About</NavLink>
              </NavigationMenuItem>
            </NavigationMenuList>
          </NavigationMenu>
        </nav>

        <div className="header-cta">
          <ThemeToggle />
          {isAuthenticated ? (
            <UserMenu />
          ) : (
            <>
              <Button className="btn-ghost" onClick={() => navigate('/login')}>
                Sign In
              </Button>
              <Button className="btn-primary" onClick={() => navigate('/signup')}>
                Sign Up
              </Button>
            </>
          )}
        </div>
      </div>
    </header>
  );
}

function Footer() {
  return (
    <footer className="site-footer">
      <div className="container footer-grid">
        <div>
          <div className="brand-inline">
            <div className="brand-mark small" />
            <span className="brand-text">EduFlow</span>
          </div>
          <p className="muted">AI-powered learning tools to master complex topics faster.</p>
        </div>
        <div className="footer-links">
          <a href="/about">About</a>
          <a href="/qa">Q&amp;A</a>
          <a href="/summarizer">Summarizer</a>
          <a href="/mcq">MCQ</a>
          <a href="/code-explainer">Code</a>
        </div>
        <div className="footer-cta">
          <p className="muted">Ready to accelerate your study flow?</p>
          <Button className="btn-primary" asChild>
            <a href="#get-started">Start Free</a>
          </Button>
        </div>
      </div>
      <div className="container copyright">© {new Date().getFullYear()} EduFlow. All rights reserved.</div>
    </footer>
  );
}

function FadeIn({ children, delay = 0, y = 12 }) {
  return (
    <motion.div initial={{ opacity: 0, y }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.5, ease: "easeOut", delay }}>
      {children}
    </motion.div>
  );
}


function Magnetic({ children, strength = 20 }) {
  const ref = React.useRef(null);
  const x = useMotionValue(0);
  const y = useMotionValue(0);
  const springX = useSpring(x, { stiffness: 180, damping: 15, mass: 0.4 });
  const springY = useSpring(y, { stiffness: 180, damping: 15, mass: 0.4 });

  React.useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const onMove = (e) => {
      const rect = el.getBoundingClientRect();
      const dx = e.clientX - (rect.left + rect.width / 2);
      const dy = e.clientY - (rect.top + rect.height / 2);
      const distX = Math.max(Math.min(dx / rect.width, 1), -1) * strength;
      const distY = Math.max(Math.min(dy / rect.height, 1), -1) * strength;
      x.set(distX);
      y.set(distY);
    };
    const onLeave = () => { x.set(0); y.set(0); };
    el.addEventListener('mousemove', onMove);
    el.addEventListener('mouseleave', onLeave);
    return () => { el.removeEventListener('mousemove', onMove); el.removeEventListener('mouseleave', onLeave); };
  }, [x, y, strength]);

  return (
    <motion.div ref={ref} style={{ display: 'inline-block', translateX: springX, translateY: springY }}>
              <motion.div className="trail" initial={{ opacity: 0 }} animate={{ opacity: 0.2 }} transition={{ duration: 0.6, ease: 'easeOut' }} />

      {children}
    </motion.div>
  );
}

function Home() {
  const navigate = useNavigate();
  const heroRef = React.useRef(null);

  React.useEffect(() => {
    const el = heroRef.current;
    if (!el) return;
    let frame = null;
    const onMove = (e) => {
      if (frame) cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        const rect = el.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;
        const px = x * 20;
        const py = y * 12;
        el.style.setProperty("--px", `${px}px`);
        el.style.setProperty("--py", `${py}px`);
      });
    };
    el.addEventListener("mousemove", onMove);
    return () => el.removeEventListener("mousemove", onMove);
  }, []);

  return (
    <main>
      {/* Hero */}
      <section className="hero" ref={heroRef}>
        <div className="container hero-grid">
          <FadeIn>
            <div className="hero-copy">
              <div className="eyebrow"><Sparkles size={16} /> AI Education, simplified</div>
              <h1>Understand anything in seconds, study smarter for hours</h1>
              <p className="lead">EduFlow turns complex topics into crystal-clear explanations, smart summaries, quizzes, and code insights—instantly.</p>
              <div className="hero-ctas" id="get-started">
                <Magnetic>
                  <Button className="btn-primary" onClick={() => navigate("/qa")}>Try Q&amp;A <ArrowRight size={16} /></Button>
                </Magnetic>
                <Magnetic strength={10}>
                  <Button className="btn-primary" onClick={() => navigate("/summarizer")}>Summarize text</Button>
                </Magnetic>
              </div>
              <div className="hero-checks">
                <div><MessageSquare size={16} /> Instant answers</div>
                <div><FileText size={16} /> Clean summaries</div>
                <div><ListChecks size={16} /> Auto MCQs</div>
                <div><Code2 size={16} /> Code explain</div>
              </div>
            </div>
          </FadeIn>
          <motion.div className="hero-visual relative" initial={{ opacity: 0, scale: 0.98 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.6, ease: "easeOut" }}>
            <div className="blob blob-1 parallax-l1" aria-hidden="true" />
            <div className="blob blob-2 parallax-l2" aria-hidden="true" />
            <motion.div className="glass hero-card parallax" whileHover={{ scale: 1.01 }} transition={{ type: "spring", stiffness: 120, damping: 14 }}>
              <img src="https://images.pexels.com/photos/9783353/pexels-photo-9783353.jpeg" alt="Abstract AI learning" className="hero-img" />
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Feature cards */}
      <section className="features" id="features">
        <div className="container">
          <div className="section-head">
            <h2>Everything you need to learn with flow</h2>
            <p className="muted">Four focused tools. One seamless workspace.</p>
          </div>
          <div className="card-grid">
            {[0,1,2,3].map((i) => (
              <FadeIn key={i} delay={0.05 * i}>
                {i === 0 && (
                  <Card className="feature-card">
                    <CardHeader>
                      <CardTitle className="card-title"><MessageSquare className="mr-2" /> AI Chat &amp; Q&amp;A</CardTitle>
                      <CardDescription>Ask anything—get structured, step-by-step answers with citations.</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <img className="feature-img" alt="Q&A" src="https://images.unsplash.com/photo-1529429612779-c8e40ef2f36d" />
                      <div className="card-actions">
                        <Magnetic strength={14}>
                          <Button className="btn-soft" onClick={() => navigate("/qa")}>Open Q&amp;A</Button>
                        </Magnetic>
                      </div>
                    </CardContent>
                  </Card>
                )}
                {i === 1 && (
                  <Card className="feature-card">
                    <CardHeader>
                      <CardTitle className="card-title"><FileText className="mr-2" /> Summarizer</CardTitle>
                      <CardDescription>Condense chapters, articles, and PDFs into concise notes.</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <img className="feature-img" alt="Summarizer" src="https://images.unsplash.com/photo-1502900476531-ca62d0f2b679" />
                      <div className="card-actions">
                        <Magnetic strength={14}>
                          <Button className="btn-soft" onClick={() => navigate("/summarizer")}>Open Summarizer</Button>
                        </Magnetic>
                      </div>
                    </CardContent>
                  </Card>
                )}
                {i === 2 && (
                  <Card className="feature-card">
                    <CardHeader>
                      <CardTitle className="card-title"><ListChecks className="mr-2" /> MCQ Generator</CardTitle>
                      <CardDescription>Create graded quizzes from any passage or topic.</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <img className="feature-img" alt="MCQ Generator" src="https://images.pexels.com/photos/4709285/pexels-photo-4709285.jpeg" />
                      <div className="card-actions">
                        <Magnetic strength={14}>
                          <Button className="btn-soft" onClick={() => navigate("/mcq")}>Open MCQ</Button>
                        </Magnetic>
                      </div>
                    </CardContent>
                  </Card>
                )}
                {i === 3 && (
                  <Card className="feature-card">
                    <CardHeader>
                      <CardTitle className="card-title"><Code2 className="mr-2" /> Code Explainer</CardTitle>
                      <CardDescription>Paste code. Get clear, commented explanations.</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <img className="feature-img" alt="Code Explainer" src="https://images.unsplash.com/photo-1529429612779-c8e40ef2f36d" />
                      <div className="card-actions">
                        <Magnetic strength={14}>
                          <Button className="btn-soft" onClick={() => navigate("/code-explainer")}>Explain Code</Button>
                        </Magnetic>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </FadeIn>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="how">
        <div className="container two-col">
          <FadeIn>
            <div>
              <h3>How EduFlow works</h3>
              <Accordion type="single" collapsible>
                <AccordionItem value="step1">
                  <AccordionTrigger>1. Add your material</AccordionTrigger>
                  <AccordionContent>Paste text, upload notes (UI only), or type a question to begin.</AccordionContent>
                </AccordionItem>
                <AccordionItem value="step2">
                  <AccordionTrigger>2. Choose a tool</AccordionTrigger>
                  <AccordionContent>Pick Q&amp;A, Summarizer, MCQ, or Code Explainer to shape the output.</AccordionContent>
                </AccordionItem>
                <AccordionItem value="step3">
                  <AccordionTrigger>3. Get instant results</AccordionTrigger>
                  <AccordionContent>Receive structured, readable content you can copy, tweak, and save.</AccordionContent>
                </AccordionItem>
              </Accordion>
            </div>
          </FadeIn>
          <FadeIn delay={0.05}>
            <div className="how-card glass">
              <div className="text-center py-12">
                <p className="text-muted-foreground mb-4">Start using EduFlow now with any of our 4 AI tools</p>
                <div className="flex flex-wrap gap-3 justify-center">
                  <NavLink to="/qa" className="btn-primary" style={{textDecoration: 'none'}}>Q&A</NavLink>
                  <NavLink to="/summarizer" className="btn-primary" style={{textDecoration: 'none'}}>Summarizer</NavLink>
                  <NavLink to="/mcq" className="btn-primary" style={{textDecoration: 'none'}}>MCQ Generator</NavLink>
                  <NavLink to="/code-explainer" className="btn-primary" style={{textDecoration: 'none'}}>Code Explainer</NavLink>
                </div>
              </div>
            </div>
          </FadeIn>
        </div>
      </section>

      {/* CTA */}
      <section className="cta">
        <div className="container cta-wrap">
          <FadeIn>
            <div>
              <h3>Study at your own pace with AI guidance</h3>
              <p className="muted">Join thousands of learners who simplify complex subjects using EduFlow.</p>
            </div>
          </FadeIn>
          <FadeIn delay={0.05}>
            <div className="cta-actions">
              <Magnetic strength={18}>
                <Button className="btn-primary" onClick={() => navigate("/qa")}><BookOpen size={16} /> Start learning</Button>
              </Magnetic>
              <Magnetic strength={12}>
                <Button className="btn-primary" onClick={() => navigate("/about")}><Play size={16} /> See how it works</Button>
              </Magnetic>
            </div>
          </FadeIn>
        </div>
      </section>
    </main>
  );
}

function PageShell({ title, subtitle, children }) {
  return (
    <main>
      <section className="page-hero">
        <div className="container">
          <h1>{title}</h1>
          {subtitle && <p className="muted">{subtitle}</p>}
        </div>
      </section>
      <section className="page-content">
        <div className="container">
          {children}
        </div>
      </section>
    </main>
  );
}

function QA() {
  const [level, setLevel] = React.useState("balanced");
  const [question, setQuestion] = React.useState("");
  const [answer, setAnswer] = React.useState("");
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState("");

  const handleGenerate = async () => {
    if (!question.trim()) {
      setError("Please enter a question");
      return;
    }

    setLoading(true);
    setError("");
    setAnswer("");

    try {
      const response = await api.post("/qa", {
        question: question.trim(),
        depth: level,
      });
      setAnswer(response.data.answer);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || "Failed to generate answer";
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageShell title="AI Q&amp;A" subtitle="Ask anything and get structured, step-by-step answers.">
      <div className="tool-grid">
        <div className="glass tool-input">
          <Label htmlFor="question">Your question</Label>
          <Textarea 
            id="question" 
            rows={6} 
            placeholder="Enter your question..." 
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <div className="row">
            <div className="select-row">
              <Label className="sr-only" htmlFor="depth">Answer depth</Label>
              <Select value={level} onValueChange={setLevel}>
                <SelectTrigger id="depth"><SelectValue placeholder="Answer depth" /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="concise">Concise</SelectItem>
                  <SelectItem value="balanced">Balanced</SelectItem>
                  <SelectItem value="detailed">Detailed</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button className="btn-primary" onClick={handleGenerate} disabled={loading}>
              {loading ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Generating...</> : "Generate"}
            </Button>
          </div>
          {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
        </div>
        <div className="tool-output">
          <Card>
            <CardHeader>
              <CardTitle>Answer</CardTitle>
              <CardDescription>{answer ? "Generated answer" : "Answer will appear here"}</CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span>Generating...</span>
                </div>
              ) : answer ? (
                <p>{answer}</p>
              ) : (
                <p className="text-muted-foreground">Ask a question and click Generate to get started</p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </PageShell>
  );
}

function Summarizer() {
  const [text, setText] = React.useState("");
  const [file, setFile] = React.useState(null);
  const [summary, setSummary] = React.useState([]);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState("");
  const [isDragging, setIsDragging] = React.useState(false);
  const [style, setStyle] = React.useState("bullet_points");
  const [maxPoints, setMaxPoints] = React.useState(5);

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
      // Read file content to show in textarea
      const reader = new FileReader();
      reader.onload = (event) => {
        setText(event.target.result);
      };
      reader.readAsText(droppedFile);
    }
  };

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      const reader = new FileReader();
      reader.onload = (event) => {
        setText(event.target.result);
      };
      reader.readAsText(selectedFile);
    }
  };

  const handleSummarize = async () => {
    if (!text.trim() && !file) {
      setError("Please enter text or upload a file");
      return;
    }

    setLoading(true);
    setError("");
    setSummary([]);

    try {
      let response;
      if (file) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('style', style);
        formData.append('max_points', maxPoints);
        response = await api.post("/v2/summarize", formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      } else {
        response = await api.post("/v2/summarize/text", {
          text: text.trim(),
          style: style,
          max_points: maxPoints,
        });
      }
      setSummary(response.data.summary);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || "Failed to summarize";
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setText("");
    setFile(null);
    setSummary([]);
    setError("");
  };

  return (
    <PageShell title="Text Summarizer" subtitle="Condense long passages into clear, actionable notes.">
      <div className="tool-grid">
        <div className="glass tool-input">
          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            className={`border-2 border-dashed rounded-lg p-4 mb-4 transition-colors ${
              isDragging ? 'border-primary bg-primary/10' : 'border-muted'
            }`}
          >
            <div className="text-center">
              <FileText className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
              <p className="text-sm text-muted-foreground mb-2">
                {file ? file.name : 'Drag and drop a file here, or click to browse'}
              </p>
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
                accept=".txt,.pdf,.doc,.docx"
                onChange={handleFileSelect}
                className="hidden"
              />
            </div>
          </div>
          <div className="space-y-2 mb-4">
            <Label htmlFor="style">Summary Style</Label>
            <Select value={style} onValueChange={setStyle}>
              <SelectTrigger id="style">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="bullet_points">Bullet Points</SelectItem>
                <SelectItem value="paragraph">Paragraph</SelectItem>
                <SelectItem value="concise">Concise</SelectItem>
                <SelectItem value="detailed">Detailed</SelectItem>
                <SelectItem value="academic">Academic</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <Label htmlFor="text">Or paste text</Label>
          <Textarea 
            id="text" 
            rows={8} 
            placeholder="Paste or type your content here..." 
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <div className="row mt-4">
            <Button className="btn-primary" onClick={handleSummarize} disabled={loading}>
              {loading ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Summarizing...</> : "Summarize"}
            </Button>
            <Button className="btn-primary" onClick={handleClear}>Clear</Button>
          </div>
          {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
        </div>
        <div className="tool-output">
          <Card>
            <CardHeader>
              <CardTitle>Summary</CardTitle>
              <CardDescription>{summary.length > 0 ? "Generated summary" : "Summary will appear here"}</CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span>Summarizing...</span>
                </div>
              ) : summary.length > 0 ? (
                <ul className="space-y-2">
                  {summary.map((point, i) => <li key={i}>• {point}</li>)}
                </ul>
              ) : (
                <p className="text-muted-foreground">Paste text and click Summarize to get started</p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </PageShell>
  );
}

function MCQ() {
  const [topic, setTopic] = React.useState("");
  const [file, setFile] = React.useState(null);
  const [questions, setQuestions] = React.useState([]);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState("");
  const [isDragging, setIsDragging] = React.useState(false);
  const [difficulty, setDifficulty] = React.useState("medium");
  const [numQuestions, setNumQuestions] = React.useState(5);

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
        setTopic(event.target.result);
      };
      reader.readAsText(droppedFile);
    }
  };

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      const reader = new FileReader();
      reader.onload = (event) => {
        setTopic(event.target.result);
      };
      reader.readAsText(selectedFile);
    }
  };

  const handleGenerate = async () => {
    if (!topic.trim() && !file) {
      setError("Please enter a topic or upload a file");
      return;
    }

    setLoading(true);
    setError("");
    setQuestions([]);

    try {
      let response;
      if (file) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('difficulty', difficulty);
        formData.append('num_questions', numQuestions);
        response = await api.post("/v2/mcq", formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      } else {
        response = await api.post("/v2/mcq/text", {
          text: topic.trim(),
          difficulty: difficulty,
          num_questions: numQuestions,
        });
      }
      setQuestions(response.data.questions);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || "Failed to generate questions";
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setTopic("");
    setFile(null);
    setQuestions([]);
    setError("");
  };

  return (
    <PageShell title="MCQ Generator" subtitle="Create quizzes from any topic and practice instantly.">
      <div className="tool-grid">
        <div className="glass tool-input">
          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            className={`border-2 border-dashed rounded-lg p-4 mb-4 transition-colors ${
              isDragging ? 'border-primary bg-primary/10' : 'border-muted'
            }`}
          >
            <div className="text-center">
              <ListChecks className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
              <p className="text-sm text-muted-foreground mb-2">
                {file ? file.name : 'Drag and drop a file here, or click to browse'}
              </p>
              <Button
                type="button"
                variant="outline"
                onClick={() => document.getElementById('mcq-file-input').click()}
              >
                Choose File
              </Button>
              <input
                id="mcq-file-input"
                type="file"
                accept=".txt,.pdf,.doc,.docx"
                onChange={handleFileSelect}
                className="hidden"
              />
            </div>
          </div>
          <div className="space-y-2 mb-4">
            <Label htmlFor="difficulty">Difficulty</Label>
            <Select value={difficulty} onValueChange={setDifficulty}>
              <SelectTrigger id="difficulty">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="easy">Easy</SelectItem>
                <SelectItem value="medium">Medium</SelectItem>
                <SelectItem value="hard">Hard</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <Label htmlFor="mcq-topic">Or enter topic/subject</Label>
          <Textarea 
            id="mcq-topic" 
            rows={6} 
            placeholder="Enter topic or subject..." 
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          />
          <div className="row mt-4">
            <Button className="btn-primary" onClick={handleGenerate} disabled={loading}>
              {loading ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Generating...</> : "Generate MCQs"}
            </Button>
            <Button className="btn-primary" onClick={handleClear}>Clear</Button>
          </div>
          {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
        </div>
        <div className="tool-output">
          <Card>
            <CardHeader>
              <CardTitle>Quiz</CardTitle>
              <CardDescription>{questions.length > 0 ? `${questions.length} questions` : "Questions will appear here"}</CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span>Generating...</span>
                </div>
              ) : questions.length > 0 ? (
                <ol className="space-y-4">
                  {questions.map((q, idx) => (
                    <li key={idx} className="border-b pb-4 last:border-b-0">
                      <p className="font-medium mb-2">{idx + 1}. {q.question}</p>
                      <ul className="space-y-1 pl-4">
                        {q.options.map((opt) => (
                          <li key={opt.letter}>{opt.letter}) {opt.text}</li>
                        ))}
                      </ul>
                      <p className="text-sm text-muted-foreground mt-2">✓ Answer: {q.correct_answer}</p>
                      <p className="text-sm mt-1">{q.explanation}</p>
                    </li>
                  ))}
                </ol>
              ) : (
                <p className="text-muted-foreground">Enter a topic and click Generate to create quiz questions</p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </PageShell>
  );
}

function CodeExplainer() {
  const [code, setCode] = React.useState("");
  const [language, setLanguage] = React.useState("python");
  const [explanation, setExplanation] = React.useState("");
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState("");

  const handleExplain = async () => {
    if (!code.trim()) {
      setError("Please enter code to explain");
      return;
    }

    setLoading(true);
    setError("");
    setExplanation("");

    try {
      const response = await api.post("/explain-code", {
        code: code.trim(),
        language: language,
      });
      setExplanation(response.data.explanation);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || "Failed to explain code";
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setCode("");
    setExplanation("");
    setError("");
  };

  return (
    <PageShell title="Code Explainer" subtitle="Paste code to get clear explanations with details.">
      <div className="tool-grid">
        <div className="glass tool-input">
          <Label htmlFor="code">Your code</Label>
          <div className="row mb-4">
            <div className="select-row">
              <Label className="sr-only" htmlFor="lang">Language</Label>
              <Select value={language} onValueChange={setLanguage}>
                <SelectTrigger id="lang"><SelectValue placeholder="Language" /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="python">Python</SelectItem>
                  <SelectItem value="javascript">JavaScript</SelectItem>
                  <SelectItem value="java">Java</SelectItem>
                  <SelectItem value="cpp">C++</SelectItem>
                  <SelectItem value="csharp">C#</SelectItem>
                  <SelectItem value="go">Go</SelectItem>
                  <SelectItem value="rust">Rust</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <Textarea 
            id="code" 
            rows={10} 
            placeholder="Paste code here..." 
            value={code}
            onChange={(e) => setCode(e.target.value)}
          />
          <div className="row">
            <Button className="btn-primary" onClick={handleExplain} disabled={loading}>
              {loading ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Explaining...</> : "Explain"}
            </Button>
            <Button className="btn-primary" onClick={handleClear}>Clear</Button>
          </div>
          {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
        </div>
        <div className="tool-output">
          <Card>
            <CardHeader>
              <CardTitle>Explanation</CardTitle>
              <CardDescription>{explanation ? "Generated explanation" : "Explanation will appear here"}</CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span>Explaining...</span>
                </div>
              ) : explanation ? (
                <pre className="code-block whitespace-pre-wrap">{explanation}</pre>
              ) : (
                <p className="text-muted-foreground">Paste code and click Explain to get started</p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </PageShell>
  );
}

function About() {
  const [isDark, setIsDark] = React.useState(() => {
    return typeof document !== 'undefined' && document.documentElement.classList.contains('theme-dark');
  });

  React.useEffect(() => {
    const checkTheme = () => {
      setIsDark(document.documentElement.classList.contains('theme-dark'));
    };
    
    const observer = new MutationObserver(checkTheme);
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
    
    return () => observer.disconnect();
  }, []);
  
  return (
    <PageShell title="About EduFlow" subtitle="Our mission is to make high-quality learning accessible and delightful.">
      <div className="about-grid">
        <Card className="glass">
          <CardHeader>
            <CardTitle style={isDark ? { color: '#ffffff' } : {}}>Mission</CardTitle>
            <CardDescription>Why we exist</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="mb-3">
              We help learners grasp complex topics faster using friendly AI. Clarity, speed, and confidence—without the overwhelm.
            </p>
            <p className="text-sm text-muted-foreground">
              Every student deserves access to personalized learning tools that adapt to their pace and style. We believe education should be empowering, not exhausting. By combining the power of AI with intuitive design, EduFlow transforms how people learn, making it easier to understand difficult concepts, retain knowledge, and build confidence in any subject.
            </p>
          </CardContent>
        </Card>
        <Card className="glass">
          <CardHeader>
            <CardTitle style={isDark ? { color: '#ffffff' } : {}}>Vision</CardTitle>
            <CardDescription>Where we&#39;re heading</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="mb-3">
              A personal AI study companion for every learner, from high school to PhD.
            </p>
            <p className="text-sm text-muted-foreground">
              We envision a future where intelligent tutoring becomes the default for learners everywhere. EduFlow is building towards a comprehensive learning ecosystem that evolves with each student—offering personalized paths, real-time feedback, and adaptive challenges that accelerate growth. Our goal is to democratize expert-level education and help every person unlock their full potential through technology and innovation.
            </p>
          </CardContent>
        </Card>
      </div>
    </PageShell>
  );
}

function NotFound() {
  return (
    <PageShell title="Page not found">
      The page you are looking for does not exist.
    </PageShell>
  );
}

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <AuthProvider>
          <Header />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/qa" element={<QA />} />
            <Route path="/summarizer" element={<Summarizer />} />
            <Route path="/mcq" element={<MCQ />} />
            <Route path="/code-explainer" element={<CodeExplainer />} />
            <Route path="/about" element={<About />} />
            
            {/* Auth Routes */}
            <Route path="/login" element={<LoginForm />} />
            <Route path="/signup" element={<SignupForm />} />
            
            {/* Protected Routes */}
            <Route 
              path="/dashboard" 
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/code-analyzer" 
              element={
                <ProtectedRoute>
                  <AdvancedCodeAnalyzer />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/profile" 
              element={
                <ProtectedRoute>
                  <ProfilePage />
                </ProtectedRoute>
              } 
            />
            
            <Route path="*" element={<NotFound />} />
          </Routes>
          <Footer />
        </AuthProvider>
      </BrowserRouter>
    </div>
  );
}

export default App;