import { useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Typewriter } from 'react-simple-typewriter';

function App() {
  const [files, setFiles] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('upload');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!files.length) return;

    const formData = new FormData();
    files.forEach((f) => formData.append("files", f));

    try {
      setLoading(true);
      setResults([]);
      const res = await axios.post('http://localhost:8000/upload', formData);
      setResults(res.data.results);
      setActiveTab('results');
    } catch (err) {
      console.error("Upload error:", err);
      alert("Upload failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const SectionCard = ({ title, children, color = "purple" }) => (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.02 }}
      className={`rounded-xl p-4 bg-white text-gray-800 shadow-md border-l-4 border-${color}-500 w-full md:w-[48%]`}
    >
      <h3 className={`text-base font-semibold text-${color}-600 mb-2`}>{title}</h3>
      <div className="text-sm">{children}</div>
    </motion.div>
  );

  const renderResults = () => (
    results.length ? results.map((res, i) => (
      <motion.div
        key={i}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: i * 0.1 }}
        className={`rounded-xl p-4 mb-10 shadow-lg bg-white text-gray-900 w-full`}
      >
        <h2 className="text-lg font-bold text-purple-700 border-b pb-2 mb-4">{res.filename}</h2>

        {res.status === "Processed" ? (
          <div className="flex flex-wrap gap-4 justify-between">

            <SectionCard title="Claim Type & Priority">
              <p><strong>Type:</strong> {res.type}</p>
              <p><strong>Priority:</strong> {res.priority}</p>
              <p><strong>Confidence:</strong> {res.confidence_score}/100</p>
              <p><strong>Reason:</strong> {res.rule_explanation}</p>
            </SectionCard>

            <SectionCard title="Intelligent Routing" color="indigo">
              <p><strong>Action:</strong> <span className="text-indigo-600 font-semibold">{res.routing_action}</span></p>
              {res.routing_log?.length > 0 && (
                <details className="mt-2">
                  <summary className="cursor-pointer text-indigo-500 font-medium">View History</summary>
                  <ul className="pl-5 mt-2 list-disc text-sm">
                    {res.routing_log.map((log, idx) => (
                      <li key={idx}>
                        <span>{log.timestamp}</span> — {log.action} <em className="text-gray-500">({log.status})</em>
                      </li>
                    ))}
                  </ul>
                </details>
              )}
            </SectionCard>

            <SectionCard title="Named Entities" color="blue">
              {res.entities?.length > 0 ? (
                <ul className="list-disc ml-5">
                  {res.entities.map((ent, idx) => (
                    <li key={idx}>{ent.text} <span className="text-gray-500">({ent.label})</span></li>
                  ))}
                </ul>
              ) : <p>No entities found.</p>}
            </SectionCard>

            <SectionCard title="Policy Compliance" color="red">
              {res.policy_violations?.length > 0 ? (
                <ul className="list-disc ml-5 text-red-700">
                  {res.policy_violations.map((v, idx) => (
                    <li key={idx}>Rule {v.rule_id}: {v.violation} ({v.category})</li>
                  ))}
                </ul>
              ) : <p className="text-green-600 font-semibold">Fully Compliant</p>}
            </SectionCard>

            <SectionCard title="Extracted Content" color="gray">
              <details className="cursor-pointer">
                <summary className="text-purple-600 font-medium">Show Text</summary>
                <pre className="bg-gray-100 mt-2 p-3 rounded max-h-60 overflow-auto text-xs whitespace-pre-wrap">{res.text}</pre>
              </details>
            </SectionCard>

          </div>
        ) : (
          <p className="text-red-600 font-bold">{res.error}</p>
        )}
      </motion.div>
    )) : (
      <SectionCard title="No Results Found">Upload a document to get started.</SectionCard>
    )
  );

  return (
  <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-800 text-white flex flex-col items-center justify-start p-6">
    <motion.h1
      className="text-4xl md:text-5xl font-extrabold text-purple-300 mb-4 text-center drop-shadow-lg"
      initial={{ opacity: 0, y: -30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <Typewriter
        words={['ClaimPilot', 'Smart Claims Engine', 'AI for Insurance']}
        loop
        cursor
        cursorStyle="_"
        typeSpeed={80}
        deleteSpeed={40}
        delaySpeed={2000}
      />
    </motion.h1>

    {/* Tab Buttons + Content */}
    <div className="flex flex-col items-center w-full max-w-5xl">
      {/* Tabs */}
      <div className="flex gap-3 flex-wrap justify-center mb-6">
        {['upload', 'results'].map(tab => (
          <motion.button
            key={tab}
            onClick={() => setActiveTab(tab)}
            whileTap={{ scale: 0.95 }}
            className={`px-5 py-2 rounded-full font-bold transition-all duration-300 ${
              activeTab === tab
                ? 'bg-purple-600 text-white shadow-md'
                : 'bg-white/10 text-purple-100 hover:bg-white/20 border border-purple-400'
            }`}
          >
            {tab === 'upload' ? 'Upload' : 'Results'}
          </motion.button>
        ))}
      </div>

      {/* Upload or Results */}
      <div className="w-full">
        {activeTab === 'upload' ? (
          <div className="flex justify-center">
            <SectionCard title="Upload Documents (PDF, DOCX, Images)">
              <form onSubmit={handleSubmit} className="text-center">
                <input
                  type="file"
                  accept=".pdf,.docx,.png,.jpg,.jpeg,.txt"
                  multiple
                  onChange={(e) => setFiles([...e.target.files])}
                  className="block w-full p-2 border border-gray-300 rounded mb-4 text-black"
                />
                <motion.button
                  type="submit"
                  disabled={loading}
                  whileTap={{ scale: 0.95 }}
                  className="bg-purple-600 hover:bg-purple-700 text-white font-bold px-6 py-2 rounded shadow-md transition disabled:opacity-50"
                >
                  {loading ? 'Analyzing...' : 'Upload & Analyze'}
                </motion.button>
              </form>
            </SectionCard>
          </div>
        ) : (
          renderResults()
        )}
      </div>
    </div>
  </div>
);

}

export default App;
