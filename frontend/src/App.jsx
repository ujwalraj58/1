import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import NET from "vanta/dist/vanta.net.min"; // Fallback effect

// Main React component for the CollegeGPT UI
export default function App() {
  // Ref for the Vanta.js background element
  const vantaRef = useRef(null);
  // Ref to store the Vanta.js effect instance
  const vantaEffect = useRef(null);

  // State for UI elements and chat functionality
  const [showTools, setShowTools] = useState(false); // Controls visibility of upload buttons
  const [inputMessage, setInputMessage] = useState(""); // State for the text input field
  const [recording, setRecording] = useState(false); // State for voice recording animation
  const [messages, setMessages] = useState([
    { text: "Hello! How can I help you today?", sender: "bot" }, // Initial bot message
  ]);
  const [isLoading, setIsLoading] = useState(false); // State for showing loading indicator
  const [tempMessage, setTempMessage] = useState(""); // Temporary message for file uploads/voice

  // useEffect hook for initializing and cleaning up Vanta.js
  useEffect(() => {
    // Check if Vanta.js effect is not already initialized and NET.default is a function
    if (!vantaEffect.current && typeof NET.default === "function") {
      vantaEffect.current = NET.default({
        el: vantaRef.current, // Element to attach the Vanta.js effect to
        THREE: THREE, // Pass THREE.js library
        mouseControls: true, // Enable mouse interaction
        touchControls: true, // Enable touch interaction
        gyroControls: false, // Disable gyro controls
        minHeight: 200.0,
        minWidth: 200.0,
        scale: 1.2,
        scaleMobile: 1.0,
        color: 0x00ffff, // Color of the net lines
        backgroundColor: 0x000000, // Background color
        points: 12.0, // Number of points in the net
        maxDistance: 25.0, // Maximum distance for lines between points
        spacing: 15.0, // Spacing between points
      });
    }

    // Cleanup function: destroy Vanta.js effect when component unmounts
    return () => {
      if (vantaEffect.current) vantaEffect.current.destroy();
    };
  }, []); // Empty dependency array ensures this runs only once on mount

  // Helper function to get CSRF token from cookies
  const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  // Function to handle sending messages to the backend
  const sendMessage = async (e) => {
    e.preventDefault(); // Prevent default form submission

    const messageText = inputMessage.trim();
    if (!messageText) return;

    // Add user message to chat history
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: messageText, sender: "user" },
    ]);
    setInputMessage(""); // Clear input field
    setIsLoading(true); // Show loading indicator

    try {
      const response = await fetch("/ask/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"), // Include CSRF token
        },
        body: JSON.stringify({ question: messageText }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.error || `HTTP error! status: ${response.status}`
        );
      }

      const data = await response.json();
      // Add bot response to chat history
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: data.answer, sender: "bot" },
      ]);
    } catch (error) {
      console.error("Error sending message:", error);
      // Display error message in chat
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: `Error: ${error.message}. Please try again.`, sender: "bot" },
      ]);
    } finally {
      setIsLoading(false); // Hide loading indicator
    }
  };

  // Voice recording simulation handlers
  const handleVoiceStart = () => {
    setRecording(true);
    setTempMessage("Listening...");
    // Simulate voice input for a few seconds
    setTimeout(() => {
      setRecording(false);
      setTempMessage(""); // Clear temporary message after "recording"
      setInputMessage("This is a simulated voice input."); // Set a sample transcript
    }, 2000);
  };

  const handleVoiceStop = () => {
    setRecording(false);
    setTempMessage("");
    // If a transcript wasn't set by timeout, clear it here
    if (inputMessage === "Listening...") {
      setInputMessage("");
    }
  };

  // File upload handlers (simulated)
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setTempMessage(`Image uploaded: ${file.name}`);
      setTimeout(() => setTempMessage(""), 3000); // Clear message after 3 seconds
    }
  };

  const handlePdfUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setTempMessage(`PDF uploaded: ${file.name} (Simulated summary)`);
      setTimeout(() => setTempMessage(""), 3000); // Clear message after 3 seconds
    }
  };

  return (
    <div
      ref={vantaRef}
      className="h-screen w-screen relative overflow-hidden text-white font-sans flex flex-col justify-between items-center p-4"
    >
      {/* Top Label */}
      <div className="absolute top-6 left-6 z-20">
        <span className="text-xs px-3 py-1 border border-white/30 rounded-full bg-white/10 backdrop-blur-md">
          College GPT
        </span>
      </div>

      {/* Center Message / Chat History */}
      <div className="flex-grow flex flex-col justify-end w-full max-w-xl p-4 overflow-y-auto z-20">
        <div className="flex flex-col gap-3">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`max-w-[80%] p-3 rounded-xl ${
                msg.sender === "user"
                  ? "bg-blue-500 self-end rounded-br-md"
                  : "bg-gray-700 self-start rounded-bl-md"
              }`}
            >
              {msg.text}
            </div>
          ))}
          {isLoading && (
            <div className="self-start text-gray-400 italic">
              AI is typing...
            </div>
          )}
        </div>
      </div>

      {/* Temporary Message Display */}
      {tempMessage && (
        <div className="absolute bottom-40 z-30 bg-white/20 text-white text-sm px-4 py-2 rounded-lg backdrop-blur-md animate-fade-in">
          {tempMessage}
        </div>
      )}

      {/* Bottom Input Bar with Slide-in Animation */}
      <form
        onSubmit={sendMessage}
        className="w-full max-w-xl flex justify-center items-center gap-4 z-20 px-4 animate-slide-up"
      >
        {/* Tools Toggle Button */}
        <div
          className="w-10 h-10 flex items-center justify-center rounded-full border border-white/30 bg-white/10 backdrop-blur-md transition-transform duration-700 ease-out hover:scale-105 cursor-pointer text-xl"
          onClick={() => setShowTools(!showTools)}
        >
          {showTools ? (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="w-6 h-6"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          ) : (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="w-6 h-6"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M12 4.5v15m7.5-7.5h-15"
              />
            </svg>
          )}
        </div>
        {/* Message Input Field */}
        <div className="flex-1 h-12 rounded-full border border-white/30 bg-white/10 backdrop-blur-md px-6 flex items-center transition-transform duration-700 ease-out hover:scale-105">
          <input
            type="text"
            placeholder="TYPE MESSAGE"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            className="bg-transparent w-full text-white placeholder-white/70 outline-none"
          />
        </div>
        {/* Voice Input Button */}
        <button
          type="button" // Important: set type="button" to prevent form submission
          className={`w-10 h-10 flex items-center justify-center rounded-full border border-white/30 bg-white/10 backdrop-blur-md transition-transform duration-700 ease-out hover:scale-105 ${
            recording ? "animate-pulse bg-red-500" : ""
          }`}
          onMouseDown={handleVoiceStart}
          onMouseUp={handleVoiceStop}
          onTouchStart={handleVoiceStart} // For touch devices
          onTouchEnd={handleVoiceStop} // For touch devices
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="w-6 h-6"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 18.75a6 6 0 0 0 6-6v-1.5m-6 7.5a6 6 0 0 1-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 0 1-3-3V8.25a3 3 0 0 1 3-3h.75a3 3 0 0 1 3 3v4.5a3 3 0 0 1-3 3H12z"
            />
          </svg>
        </button>
      </form>

      {/* Pop-up Upload Buttons */}
      {showTools && (
        <div className="absolute bottom-24 left-6 z-30 flex gap-4 animate-fade-in">
          <label className="cursor-pointer p-3 rounded-2xl border border-white/30 bg-white/10 backdrop-blur-md text-white text-xs transition-transform duration-500 hover:scale-105 flex items-center justify-center gap-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="w-4 h-4"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M2.25 15.75l1.5 1.5m1.5-1.5l1.5 1.5m7.5-6l3-3m0 0l3 3m-3-3v12.75A2.25 2.25 0 0118 21H6a2.25 2.25 0 01-2.25-2.25V6.75A2.25 2.25 0 016 4.5h12.75a2.25 2.25 0 012.25 2.25v7.5"
              />
            </svg>
            Image
            <input
              type="file"
              accept="image/*"
              hidden
              onChange={handleFileUpload}
            />
          </label>
          <label className="cursor-pointer p-3 rounded-2xl border border-white/30 bg-white/10 backdrop-blur-md text-white text-xs transition-transform duration-500 hover:scale-105 flex items-center justify-center gap-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="w-4 h-4"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m.75 12l3 3m0 0l3-3m-3 3V2.25"
              />
            </svg>
            PDF
            <input
              type="file"
              accept="application/pdf"
              hidden
              onChange={handlePdfUpload}
            />
          </label>
        </div>
      )}

      {/* Custom Slide/Fade Animations */}
      <style jsx>{`
        .animate-slide-up {
          animation: slideUp 1s ease-out forwards;
        }
        .animate-fade-in {
          animation: fadeIn 0.8s ease-in forwards;
        }
        .animate-pulse {
          animation: pulse 1.5s infinite ease-in-out;
        }
        @keyframes slideUp {
          0% {
            transform: translateY(100%);
            opacity: 0;
          }
          100% {
            transform: translateY(0);
            opacity: 1;
          }
        }
        @keyframes fadeIn {
          0% {
            opacity: 0;
            transform: scale(0.9);
          }
          100% {
            opacity: 1;
            transform: scale(1);
          }
        }
        @keyframes pulse {
          0%,
          100% {
            transform: scale(1);
            opacity: 1;
          }
          50% {
            transform: scale(1.1);
            opacity: 0.7;
          }
        }
      `}</style>
    </div>
  );
}
