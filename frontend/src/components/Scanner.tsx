import { Html5Qrcode } from "html5-qrcode";
import { useState } from "react";
import { motion } from "framer-motion";

export default function Scanner({ onScan }: { onScan: (raw: string) => void }) {
  const [active, setActive] = useState(false);

  const start = () => {
    setActive(true);
    const qr = new Html5Qrcode("reader");
    qr.start(
      { facingMode: "environment" },
      { fps: 10, qrbox: 250 },
      (msg) => {
        qr.stop();
        setActive(false);
        onScan(msg);
      }
    ).catch(() => setActive(false));
  };

  return (
    <motion.div initial={{ scale: 0.9 }} animate={{ scale: 1 }}>
      <button
        className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-xl shadow-lg font-bold"
        onClick={start}
      >
        {active ? "Scanning..." : "Start Scan 📷"}
      </button>
      <div id="reader" className={active ? "mt-4" : "hidden"} />
    </motion.div>
  );
}
