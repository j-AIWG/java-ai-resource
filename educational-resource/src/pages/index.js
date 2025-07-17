import React from 'react';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import '../css/custom.css';

export default function Home() {
  return (
    <Layout title="Java + AI Resource Hub">
      <div className="homepage">
        <main className="container" style={{ maxWidth: '900px', margin: '0 auto', padding: '2rem' }}>
          <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>
            Java + AI Resource Hub
          </h1>
          
          <p style={{ fontSize: '1.2rem', marginBottom: '2rem' }}>
            Welcome! Whether you're a <strong>Java developer</strong> exploring AI, an <strong>AI engineer</strong> looking to leverage Java, or a <strong>teacher</strong> looking to teach AI to your students,
            this hub helps you connect the dots. Dive into practical guides, concepts, and many code examples to get you started in no time.
          </p>

          {/* Getting Started */}
          <section style={{ marginBottom: '3rem' }}>
            <h2 style={{ fontSize: '2rem', marginBottom: '1rem' }}>🚀 Getting Started</h2>
            <ul style={{ listStyle: 'none', paddingLeft: 0, fontSize: '1.15rem' }}>
              <li style={{ marginBottom: '1rem' }}>
                <Link to="/docs/genai" style={{ textDecoration: 'none' }}>
                  <span role="img" aria-label="GenAI" style={{ marginRight: '0.5em' }}>🤖</span>
                  <strong>GenAI</strong> <span style={{ color: '#888' }}>(LLMs, Chatbots and more)</span>
                </Link>
              </li>
              <li style={{ marginBottom: '1rem' }}>
                <Link to="/docs/ml" style={{ textDecoration: 'none' }}>
                  <span role="img" aria-label="ML" style={{ marginRight: '0.5em' }}>📊</span>
                  <strong>ML</strong> <span style={{ color: '#888' }}>(Training, Datasets, Image Recognition and more)</span>
                </Link>
              </li>
              <li style={{ marginBottom: '1rem' }}>
                <Link to="/docs/agentic-ai" style={{ textDecoration: 'none' }}>
                  <span role="img" aria-label="Agentic AI" style={{ marginRight: '0.5em' }}>🦾</span>
                  <strong>Agentic AI</strong> <span style={{ color: '#888' }}>(that will coordinate and execute code and tasks for you)</span>
                </Link>
              </li>
              <li style={{ marginBottom: '1rem' }}>
                <Link to="/docs/ai-assisted-coding" style={{ textDecoration: 'none' }}>
                  <span role="img" aria-label="AI-assisted Coding" style={{ marginRight: '0.5em' }}>💡</span>
                  <strong>AI-assisted Coding</strong> <span style={{ color: '#888' }}>(tools that use AI to help you write code and apps)</span>
                </Link>
              </li>
              <li style={{ marginBottom: '1rem', marginTop: '1.5rem' }}>
                <Link to="/docs/full-sitemap" style={{
                  display: 'inline-block',
                  background: 'rgba(230, 242, 255, 0.7)',
                  border: '1.5px solid #3399ff',
                  borderRadius: '0.5em',
                  padding: '0.5em 1.2em',
                  fontWeight: 'bold',
                  fontSize: '1.18rem',
                  color: '#1565c0',
                  letterSpacing: '0.03em',
                  boxShadow: '0 1px 6px 0 rgba(51,153,255,0.07)',
                  textTransform: 'uppercase',
                  textAlign: 'center',
                  transition: 'background 0.2s, color 0.2s',
                }}>
                  <span role="img" aria-label="Sitemap" style={{ fontSize: '1.3em', verticalAlign: 'middle', marginRight: '0.5rem' }}>🗺️</span>
                  OR EXPLORE THE FULL SITEMAP
                </Link>
              </li>
            </ul>
          </section>

          {/* Hot Topics */}
          <section style={{ marginBottom: '3rem' }}>
            <h2 style={{ fontSize: '2rem', marginBottom: '1rem' }}>🔥 Hot Topics</h2>
            <ul style={{ listStyle: 'none', paddingLeft: 0, columnCount: 2, columnGap: '2rem' }}>
              <li style={{
                marginBottom: '1.2rem',
                breakInside: 'avoid',
                background: 'rgba(255, 236, 179, 0.7)',
                border: '1.5px solid #ff9800',
                borderRadius: '0.5em',
                padding: '0.6em 1em',
                fontWeight: 'bold',
                fontSize: '1.08rem',
                color: '#e65100',
                letterSpacing: '0.01em',
                boxShadow: '0 1px 6px 0 rgba(255,152,0,0.07)',
                textAlign: 'left',
                transition: 'background 0.2s, color 0.2s',
                display: 'block',
              }}><Link to="/docs/ml/architectures/neural-networks" style={{ color: 'inherit', textDecoration: 'none' }}><strong>Neural Networks</strong></Link></li>
              <li style={{
                marginBottom: '1.2rem',
                breakInside: 'avoid',
                background: 'rgba(255, 236, 179, 0.7)',
                border: '1.5px solid #ff9800',
                borderRadius: '0.5em',
                padding: '0.6em 1em',
                fontWeight: 'bold',
                fontSize: '1.08rem',
                color: '#e65100',
                letterSpacing: '0.01em',
                boxShadow: '0 1px 6px 0 rgba(255,152,0,0.07)',
                textAlign: 'left',
                transition: 'background 0.2s, color 0.2s',
                display: 'block',
              }}><Link to="/docs/genai/using-llms-in-code/functionality/content-retrieval" style={{ color: 'inherit', textDecoration: 'none' }}><strong>RAG (Retrieval-Augmented Generation)</strong></Link></li>
              <li style={{
                marginBottom: '1.2rem',
                breakInside: 'avoid',
                background: 'rgba(255, 236, 179, 0.7)',
                border: '1.5px solid #ff9800',
                borderRadius: '0.5em',
                padding: '0.6em 1em',
                fontWeight: 'bold',
                fontSize: '1.08rem',
                color: '#e65100',
                letterSpacing: '0.01em',
                boxShadow: '0 1px 6px 0 rgba(255,152,0,0.07)',
                textAlign: 'left',
                transition: 'background 0.2s, color 0.2s',
                display: 'block',
              }}><Link to="/docs/genai/using-llms-in-code/functionality/content-retrieval/vector-dbs" style={{ color: 'inherit', textDecoration: 'none' }}><strong>Vector Databases</strong></Link></li>
              <li style={{
                marginBottom: '1.2rem',
                breakInside: 'avoid',
                background: 'rgba(255, 236, 179, 0.7)',
                border: '1.5px solid #ff9800',
                borderRadius: '0.5em',
                padding: '0.6em 1em',
                fontWeight: 'bold',
                fontSize: '1.08rem',
                color: '#e65100',
                letterSpacing: '0.01em',
                boxShadow: '0 1px 6px 0 rgba(255,152,0,0.07)',
                textAlign: 'left',
                transition: 'background 0.2s, color 0.2s',
                display: 'block',
              }}><Link to="/docs/genai/using-llms-in-code/functionality/tool-calling" style={{ color: 'inherit', textDecoration: 'none' }}><strong>Tool / Function Calling</strong></Link></li>
              <li style={{
                marginBottom: '1.2rem',
                breakInside: 'avoid',
                background: 'rgba(255, 236, 179, 0.7)',
                border: '1.5px solid #ff9800',
                borderRadius: '0.5em',
                padding: '0.6em 1em',
                fontWeight: 'bold',
                fontSize: '1.08rem',
                color: '#e65100',
                letterSpacing: '0.01em',
                boxShadow: '0 1px 6px 0 rgba(255,152,0,0.07)',
                textAlign: 'left',
                transition: 'background 0.2s, color 0.2s',
                display: 'block',
              }}><Link to="/docs/agentic-ai" style={{ color: 'inherit', textDecoration: 'none' }}><strong>Agents</strong></Link></li>
              <li style={{
                marginBottom: '1.2rem',
                breakInside: 'avoid',
                background: 'rgba(255, 236, 179, 0.7)',
                border: '1.5px solid #ff9800',
                borderRadius: '0.5em',
                padding: '0.6em 1em',
                fontWeight: 'bold',
                fontSize: '1.08rem',
                color: '#e65100',
                letterSpacing: '0.01em',
                boxShadow: '0 1px 6px 0 rgba(255,152,0,0.07)',
                textAlign: 'left',
                transition: 'background 0.2s, color 0.2s',
                display: 'block',
              }}><Link to="/docs/genai/using-llms-in-code/functionality/chatbots" style={{ color: 'inherit', textDecoration: 'none' }}><strong>Chatbots</strong></Link></li>
              <li style={{
                marginBottom: '1.2rem',
                breakInside: 'avoid',
                background: 'rgba(255, 236, 179, 0.7)',
                border: '1.5px solid #ff9800',
                borderRadius: '0.5em',
                padding: '0.6em 1em',
                fontWeight: 'bold',
                fontSize: '1.08rem',
                color: '#e65100',
                letterSpacing: '0.01em',
                boxShadow: '0 1px 6px 0 rgba(255,152,0,0.07)',
                textAlign: 'left',
                transition: 'background 0.2s, color 0.2s',
                display: 'block',
              }}><Link to="/docs/genai/inference" style={{ color: 'inherit', textDecoration: 'none' }}><strong>Model Inference</strong></Link></li>
              <li style={{
                marginBottom: '1.2rem',
                breakInside: 'avoid',
                background: 'rgba(255, 236, 179, 0.7)',
                border: '1.5px solid #ff9800',
                borderRadius: '0.5em',
                padding: '0.6em 1em',
                fontWeight: 'bold',
                fontSize: '1.08rem',
                color: '#e65100',
                letterSpacing: '0.01em',
                boxShadow: '0 1px 6px 0 rgba(255,152,0,0.07)',
                textAlign: 'left',
                transition: 'background 0.2s, color 0.2s',
                display: 'block',
              }}><Link to="/docs/ml/training" style={{ color: 'inherit', textDecoration: 'none' }}><strong>Training Models</strong></Link></li>
            </ul>
          </section>

          {/* Learning Paths */}
          <section style={{ marginBottom: '3rem' }}>
            <h2 style={{ fontSize: '2rem', marginBottom: '1rem' }}>🧑‍🎓 Learning Paths (Coming Soon)</h2>
            <p style={{ fontSize: '1.1rem' }}>
              Structured learning journeys to help you get started faster:
            </p>
            <ul style={{ listStyle: 'none', paddingLeft: 0, columnCount: 2, columnGap: '2rem' }}>
              <li style={{
                marginBottom: '1.2rem',
                breakInside: 'avoid',
                background: 'rgba(232, 245, 233, 0.7)',
                border: '1.5px solid #4caf50',
                borderRadius: '0.5em',
                padding: '0.6em 1em',
                fontWeight: 'bold',
                fontSize: '1.08rem',
                color: '#2e7d32',
                letterSpacing: '0.01em',
                boxShadow: '0 1px 6px 0 rgba(76,175,80,0.07)',
                textAlign: 'left',
                transition: 'background 0.2s, color 0.2s',
                display: 'block',
              }}><Link to="/docs/learning-paths/new-to-java" style={{ color: 'inherit', textDecoration: 'none' }}><strong>New to Java</strong></Link></li>
              <li style={{
                marginBottom: '1.2rem',
                breakInside: 'avoid',
                background: 'rgba(232, 245, 233, 0.7)',
                border: '1.5px solid #4caf50',
                borderRadius: '0.5em',
                padding: '0.6em 1em',
                fontWeight: 'bold',
                fontSize: '1.08rem',
                color: '#2e7d32',
                letterSpacing: '0.01em',
                boxShadow: '0 1px 6px 0 rgba(76,175,80,0.07)',
                textAlign: 'left',
                transition: 'background 0.2s, color 0.2s',
                display: 'block',
              }}><Link to="/docs/learning-paths/new-to-ai" style={{ color: 'inherit', textDecoration: 'none' }}><strong>New to AI</strong></Link></li>
              <li style={{
                marginBottom: '1.2rem',
                breakInside: 'avoid',
                background: 'rgba(232, 245, 233, 0.7)',
                border: '1.5px solid #4caf50',
                borderRadius: '0.5em',
                padding: '0.6em 1em',
                fontWeight: 'bold',
                fontSize: '1.08rem',
                color: '#2e7d32',
                letterSpacing: '0.01em',
                boxShadow: '0 1px 6px 0 rgba(76,175,80,0.07)',
                textAlign: 'left',
                transition: 'background 0.2s, color 0.2s',
                display: 'block',
              }}><Link to="/docs/learning-paths/new-to-ml" style={{ color: 'inherit', textDecoration: 'none' }}><strong>New to ML</strong></Link></li>
              <li style={{
                marginBottom: '1.2rem',
                breakInside: 'avoid',
                background: 'rgba(232, 245, 233, 0.7)',
                border: '1.5px solid #4caf50',
                borderRadius: '0.5em',
                padding: '0.6em 1em',
                fontWeight: 'bold',
                fontSize: '1.08rem',
                color: '#2e7d32',
                letterSpacing: '0.01em',
                boxShadow: '0 1px 6px 0 rgba(76,175,80,0.07)',
                textAlign: 'left',
                transition: 'background 0.2s, color 0.2s',
                display: 'block',
              }}><Link to="/docs/learning-paths/training-first-model" style={{ color: 'inherit', textDecoration: 'none' }}><strong>Training Your First Model</strong></Link></li>
              <li style={{
                marginBottom: '1.2rem',
                breakInside: 'avoid',
                background: 'rgba(232, 245, 233, 0.7)',
                border: '1.5px solid #4caf50',
                borderRadius: '0.5em',
                padding: '0.6em 1em',
                fontWeight: 'bold',
                fontSize: '1.08rem',
                color: '#2e7d32',
                letterSpacing: '0.01em',
                boxShadow: '0 1px 6px 0 rgba(76,175,80,0.07)',
                textAlign: 'left',
                transition: 'background 0.2s, color 0.2s',
                display: 'block',
              }}><Link to="/docs/learning-paths/building-first-ai-app" style={{ color: 'inherit', textDecoration: 'none' }}><strong>Building Your First AI-Powered App</strong></Link></li>
              <li style={{
                marginBottom: '1.2rem',
                breakInside: 'avoid',
                background: 'rgba(232, 245, 233, 0.7)',
                border: '1.5px solid #4caf50',
                borderRadius: '0.5em',
                padding: '0.6em 1em',
                fontWeight: 'bold',
                fontSize: '1.08rem',
                color: '#2e7d32',
                letterSpacing: '0.01em',
                boxShadow: '0 1px 6px 0 rgba(76,175,80,0.07)',
                textAlign: 'left',
                transition: 'background 0.2s, color 0.2s',
                display: 'block',
              }}><Link to="/docs/learning-paths/langchain4j-tutorial" style={{ color: 'inherit', textDecoration: 'none' }}><strong>LangChain4j Tutorial</strong></Link></li>
              <li style={{
                marginBottom: '1.2rem',
                breakInside: 'avoid',
                background: 'rgba(232, 245, 233, 0.7)',
                border: '1.5px solid #4caf50',
                borderRadius: '0.5em',
                padding: '0.6em 1em',
                fontWeight: 'bold',
                fontSize: '1.08rem',
                color: '#2e7d32',
                letterSpacing: '0.01em',
                boxShadow: '0 1px 6px 0 rgba(76,175,80,0.07)',
                textAlign: 'left',
                transition: 'background 0.2s, color 0.2s',
                display: 'block',
              }}><Link to="/docs/learning-paths/spring-ai-tutorial" style={{ color: 'inherit', textDecoration: 'none' }}><strong>Spring AI Tutorial</strong></Link></li>
              <li style={{
                marginBottom: '1.2rem',
                breakInside: 'avoid',
                background: 'rgba(232, 245, 233, 0.7)',
                border: '1.5px solid #4caf50',
                borderRadius: '0.5em',
                padding: '0.6em 1em',
                fontWeight: 'bold',
                fontSize: '1.08rem',
                color: '#2e7d32',
                letterSpacing: '0.01em',
                boxShadow: '0 1px 6px 0 rgba(76,175,80,0.07)',
                textAlign: 'left',
                transition: 'background 0.2s, color 0.2s',
                display: 'block',
              }}><Link to="/docs/learning-paths/finetune-your-first-model" style={{ color: 'inherit', textDecoration: 'none' }}><strong>Finetune Your First Model</strong></Link></li>
            </ul>
            <p style={{ fontSize: '1.1rem', fontStyle: 'italic' }}>
              These learning paths are under development. Check back soon for complete guides!
            </p>
          </section>

          {/* Domain Use Cases */}
          <section style={{ marginBottom: '3rem' }}>
            <h2 style={{ fontSize: '2rem', marginBottom: '1rem' }}>🧩 AI for Your Domain</h2>
            <p style={{ fontSize: '1.1rem' }}>
              Explore how Java + AI fits into specific industries:
            </p>
            <ul style={{ listStyle: 'none', paddingLeft: 0, columnCount: 2, columnGap: '2rem' }}>
              <li><Link to="/docs/domain-use-cases/finance"><strong>Finance</strong></Link></li>
              <li><Link to="/docs/domain-use-cases/healthcare"><strong>Healthcare</strong></Link></li>
              <li><Link to="/docs/domain-use-cases/accessibility"><strong>Accessibility</strong></Link></li>
              <li><Link to="/docs/domain-use-cases/scientific-research"><strong>Scientific Research</strong></Link></li>
              <li><Link to="/docs/domain-use-cases/education"><strong>Education</strong></Link></li>
              <li><Link to="/docs/domain-use-cases/ecommerce"><strong>eCommerce</strong></Link></li>
            </ul>
          </section>

          <p style={{ fontStyle: 'italic', fontSize: '1rem' }}>
            P.S. This site is growing—new tutorials and learning paths will keep arriving!
          </p>
        </main>
      </div>
    </Layout>
  );
}
