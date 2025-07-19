import { useState } from "react";
import Scanner from "./components/Scanner";
import { AnimatePresence, motion } from "framer-motion";
import axios from "axios";

type Scan = { result: string; order: string; tag: string };

function App() {
  const [scans, setScans] = useState<Scan[]>([]);
  const [summary, setSummary] = useState<Record<string, number>>({});

  const handleScan = async (raw: string) => {
    try {
      const { data } = await axios.post<Scan>("/api/scan", raw, {
        headers: { "Content-Type": "text/plain" },
      });
      setScans((s) => [data, ...s.slice(0, 19)]);
      const { data: sm } = await axios.get<Record<string, number>>("/api/tag-summary");
      setSummary(sm);
    } catch {
      alert("Scan failed");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-400 to-purple-600 text-gray-900 p-4 flex flex-col items-center">
      <h1 className="text-4xl font-extrabold text-white drop-shadow-lg mb-6">
        📦 Order Scanner
      </h1>
      <Scanner onScan={handleScan} />
      <div className="w-full max-w-2xl mt-8 space-y-6">
        <section className="bg-white/80 backdrop-blur rounded-2xl p-6 shadow-xl">
          <h2 className="text-2xl font-bold mb-4">Recent Scans</h2>
          <ul className="space-y-3 max-h-[300px] overflow-y-auto">
            <AnimatePresence>
              {scans.map((s) => (
                <motion.li
                  key={s.order}
                  initial={{ y: -10, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  exit={{ y: 10, opacity: 0 }}
                  className={
                    "p-4 rounded-xl shadow " +
                    (s.result.includes("✅")
                      ? "bg-green-100 border-l-4 border-green-500"
                      : s.result.includes("⚠️")
                      ? "bg-yellow-100 border-l-4 border-yellow-500"
                      : "bg-red-100 border-l-4 border-red-500")
                  }
                >
                  <div className="font-semibold">{s.result}</div>
                  <div className="text-xl font-mono">{s.order}</div>
                  <span className="inline-block mt-2 px-3 py-1 rounded-full bg-gray-200 text-sm uppercase">
                    {s.tag || "NO TAG"}
                  </span>
                </motion.li>
              ))}
            </AnimatePresence>
          </ul>
        </section>
        <section className="bg-white/80 backdrop-blur rounded-2xl p-6 shadow-xl">
          <h2 className="text-2xl font-bold mb-4">Tag Summary</h2>
          <div className="flex flex-wrap gap-4">
            {Object.entries(summary)
              .sort((a, b) => b[1] - a[1])
              .map(([tag, n]) => (
                <span
                  key={tag}
                  className="px-4 py-2 rounded-full bg-indigo-200 font-semibold"
                >
                  {n} × {tag}
                </span>
              ))}
          </div>
        </section>
      </div>
    </div>
  );
}
export default App;
