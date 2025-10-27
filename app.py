import React, { useState, useEffect } from "react";
import { evaluate } from "mathjs";

// Default export React component. TailwindCSS classes are used for styling.
export default function ScientificCalculator() {
  const [expr, setExpr] = useState("");
  const [result, setResult] = useState("");
  const [dark, setDark] = useState(true);

  useEffect(() => {
    // live preview (try/catch to avoid noisy errors)
    try {
      if (expr.trim() === "") {
        setResult("");
        return;
      }
      const safe = normalizeExpression(expr);
      const val = evaluate(safe);
      setResult(String(val));
    } catch (e) {
      setResult("");
    }
  }, [expr]);

  function normalizeExpression(s) {
    // Replace UI-friendly tokens with mathjs-friendly ones
    return s
      .replace(/×/g, "*")
      .replace(/÷/g, "/")
      .replace(/π/g, "pi")
      .replace(/e/g, "e")
      .replace(/√/g, "sqrt")
      .replace(/\^/g, "^")
      .replace(/--/g, "+");
  }

  function append(token) {
    setExpr((p) => p + token);
  }

  function pressFunc(name) {
    // functions add '(' after them
    if (name === "!") {
      // factorial is postfix
      append("!");
      return;
    }
    append(name + "(");
  }

  function clearAll() {
    setExpr("");
    setResult("");
  }

  function backspace() {
    setExpr((p) => p.slice(0, -1));
  }

  function calculate() {
    try {
      const safe = normalizeExpression(expr);
      const val = evaluate(safe);
      setResult(String(val));
      setExpr(String(val));
    } catch (e) {
      setResult("Error");
    }
  }

  function handleKey(e) {
    // basic keyboard support
    const key = e.key;
    if ((/\d/).test(key)) return append(key);
    if (key === "+" || key === "-" || key === "/" || key === "*") return append(key);
    if (key === "Enter") return calculate();
    if (key === "Backspace") return backspace();
    if (key === ".") return append('.');
    if (key === "(") return append('(');
    if (key === ")") return append(')');
  }

  useEffect(() => {
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, []);

  // button definitions in rows (to make layout simple)
  const buttons = [
    ["sin", "cos", "tan", "ln", "log"],
    ["7", "8", "9", "(", ")"],
    ["4", "5", "6", "×", "÷"],
    ["1", "2", "3", "+", "-"],
    ["0", ".", "^", "π", "e"],
    ["!", "√", "Ans", "DEL", "C"]
  ];

  return (
    <div className={dark ? "min-h-screen flex items-center justify-center bg-gray-900" : "min-h-screen flex items-center justify-center bg-gray-100"}>
      <div className={dark ? "w-[420px] p-6 rounded-2xl bg-gradient-to-br from-gray-800 to-gray-900 shadow-2xl" : "w-[420px] p-6 rounded-2xl bg-white shadow-lg"}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className={dark ? "text-white text-xl font-semibold" : "text-gray-800 text-xl font-semibold"}>Scientific Calculator</h1>
            <p className={dark ? "text-gray-400 text-sm" : "text-gray-500 text-sm"}>Sin, Cos, Tan, !, π, e, sqrt, ^</p>
          </div>
          <div className="flex items-center gap-2">
            <button onClick={() => setDark(!dark)} className={dark ? "px-3 py-1 rounded-full bg-gray-700 text-white" : "px-3 py-1 rounded-full bg-gray-200 text-gray-800"}>{dark ? 'Dark' : 'Light'}</button>
          </div>
        </div>

        <div className={dark ? "rounded-xl p-4 mb-4 bg-gray-800 text-right" : "rounded-xl p-4 mb-4 bg-gray-50 text-right"}>
          <div className={dark ? "text-gray-400 text-sm break-words min-h-[28px]" : "text-gray-500 text-sm break-words min-h-[28px]"}>{expr || '0'}</div>
          <div className={dark ? "text-white text-2xl font-medium mt-2" : "text-gray-900 text-2xl font-medium mt-2"}>{result || ''}</div>
        </div>

        <div className="grid grid-cols-5 gap-3">
          {buttons.flat().map((b) => (
            <button
              key={b}
              onClick={() => {
                if (b === 'C') return clearAll();
                if (b === 'DEL') return backspace();
                if (b === 'Ans') return append(result ? result : '');
                if (['sin','cos','tan','ln','log','√'].includes(b)) return pressFunc(b === '√' ? 'sqrt' : b);
                if (b === 'π') return append('π');
                if (b === 'e') return append('e');
                if (b === '!') return pressFunc('!');
                if (b === '^') return append('^');
                // default append
                append(b);
              }}
              className={
                `py-3 rounded-xl text-sm font-medium shadow-inner focus:outline-none transition-all ` +
                (b === 'C' ? (dark ? 'bg-red-500 text-white' : 'bg-red-400 text-white') :
                 b === 'DEL' ? (dark ? 'bg-yellow-600 text-white' : 'bg-yellow-500 text-white') :
                 ['+','-','×','÷','^','!'].includes(b) ? (dark ? 'bg-orange-500 text-white' : 'bg-orange-400 text-white') :
                 (dark ? 'bg-gray-700 text-white' : 'bg-gray-100 text-gray-800'))
              }
            >
              {b}
            </button>
          ))}

          {/* Equals button spanning full width at bottom */}
          <button onClick={calculate} className="col-span-5 mt-2 py-3 rounded-xl text-lg font-semibold bg-indigo-600 text-white">=</button>
        </div>

        <div className="mt-4 text-xs text-center text-gray-400">
          Tip: Use keyboard for numbers and operators. Press Enter for =.
        </div>
      </div>
    </div>
  );
}

