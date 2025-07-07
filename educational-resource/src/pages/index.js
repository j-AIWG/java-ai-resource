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
            </ul>
          </section>

          {/* Hot Topics */}
          <section style={{ marginBottom: '3rem' }}>
            <h2 style={{ fontSize: '2rem', marginBottom: '1rem' }}>🔥 Hot Topics</h2>
            <ul style={{ listStyle: 'none', paddingLeft: 0, columnCount: 2, columnGap: '2rem' }}>
              <li><Link to="/docs/ml/architectures/neural-networks"><strong>Neural Networks</strong></Link></li>
              <li><Link to="/docs/genai/using-llms-in-code/functionality/content-retrieval"><strong>RAG (Retrieval-Augmented Generation)</strong></Link></li>
              <li><Link to="/docs/genai/using-llms-in-code/functionality/content-retrieval/vector-dbs"><strong>Vector Databases</strong></Link></li>
              <li><Link to="/docs/genai/using-llms-in-code/functionality/tool-calling"><strong>Tool / Function Calling</strong></Link></li>
              <li><Link to="/docs/agentic-ai"><strong>Agents</strong></Link></li>
              <li><Link to="/docs/genai/using-llms-in-code/functionality/chatbots"><strong>Chatbots</strong></Link></li>
              <li><Link to="/docs/genai/inference"><strong>Model Inference</strong></Link></li>
              <li><Link to="/docs/ml/training"><strong>Training Models</strong></Link></li>
            </ul>
          </section>

          {/* Coming Soon */}
          <section style={{ marginBottom: '3rem' }}>
            <h2 style={{ fontSize: '2rem', marginBottom: '1rem' }}>🧑‍🎓 Learning Paths (Coming Soon)</h2>
            <p style={{ fontSize: '1.1rem' }}>
              We're working on tailored learning journeys, including:
            </p>
            <ul style={{ listStyle: 'disc', paddingLeft: '1.5rem' }}>
              <li><strong>New to Java</strong></li>
              <li><strong>New to AI</strong></li>
              <li><strong>New to ML</strong></li>
              <li><strong>Training Your First Model</strong></li>
              <li><strong>Building Your First AI-Powered App</strong></li>
              <li><strong>LangChain4j Tutorial</strong></li>
              <li><strong>Spring AI Tutorial</strong></li>
            </ul>
            <p style={{ fontSize: '1.1rem' }}>
              Check back soon for structured guides to help you get started faster!
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
