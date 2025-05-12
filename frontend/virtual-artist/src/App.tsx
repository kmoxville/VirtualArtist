import React, { useState, useRef } from 'react';
import axios from 'axios';

const App: React.FC = () => {
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);

    chunksRef.current = [];

    mediaRecorder.ondataavailable = (event: BlobEvent) => {
      if (event.data.size > 0) {
        chunksRef.current.push(event.data);
      }
    };

    mediaRecorder.onstop = async () => {
      const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
      await sendToBackend(blob);
    };

    mediaRecorderRef.current = mediaRecorder;
    mediaRecorder.start();
    setIsRecording(true);
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    mediaRecorderRef.current?.stream.getTracks().forEach(track => track.stop());
    setIsRecording(false);
  };

  const sendToBackend = async (blob: Blob) => {
    const formData = new FormData();
    formData.append('file', blob, 'audio.webm');

    try {
      await axios.post('http://localhost:8000/api/v1/audio/audio/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      await playResponseAudio();
    } catch (err) {
      console.error('Ошибка при отправке аудио:', err);
    }
  };

  const playResponseAudio = async () => {
    try {
      const response = await axios.get('http://localhost:8000/audio/response-audio/', {
        responseType: 'blob',
      });

      const audioUrl = URL.createObjectURL(response.data);
      const audio = new Audio(audioUrl);
      audio.play();
    } catch (err) {
      console.error('Ошибка при получении аудио:', err);
    }
  };

  return (
    <div style={{ padding: 40 }}>
      <h1>🎤 Виртуальный артист</h1>
      <button onClick={isRecording ? stopRecording : startRecording}>
        {isRecording ? '🛑 Остановить' : '🔴 Начать запись'}
      </button>
      <br />
      <button onClick={playResponseAudio} style={{ marginTop: 20 }}>
        ▶️ Воспроизвести ответ
      </button>
    </div>
  );
};

export default App;