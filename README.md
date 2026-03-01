# Context-Aware Voice Agent 

A low-latency, WebRTC-based voice assistant demo version. This project demonstrates real-time speech-to-speech interaction with deterministic grounding and edge-optimized inference.

## Technical Architecture

To achieve sub-second turn-taking, the system utilizes a hybrid edge-cloud architecture:

* **Edge Inference (STT & TTS):** We use **Moonshine (STT)** and **Kokoro (TTS)** running locally. Processing audio on the edge eliminates the latency overhead of sending raw audio buffers to the cloud.
* **Inference Engine:** **Groq (Llama 3.1 8B Instant)** is utilized for the LLM layer, chosen for its industry-leading Token-per-Second (TPS) throughput and low Time-To-First-Token (TTFT).
* **WebRTC Framework:** **FastRTC** handles the media streaming and signaling. 
* **Grounding Layer:** Implements a deterministic context injection via `project_info.txt` to ensure the agent remains grounded in specific project data while retaining general reasoning capabilities.

## Infrastructure & Connectivity

* **NAT Traversal:** Configured with Google STUN servers to ensure reliable WebRTC handshakes across restrictive enterprise and mobile network firewalls.
* **VAD Optimization:** Integrated Silero VAD with a tuned 800ms silence threshold for natural, human-like turn-taking.


## Clone the Repo:
   ```bash
   git clone [https://github.com/KanishDhiman02/Contextual-LLM-using-FASTRTC.git](https://github.com/KanishDhiman02/Contextual-LLM-using-FASTRTC.git)
   cd Contextual-LLM-using-FASTRTC
