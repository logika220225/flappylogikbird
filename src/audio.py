import threading
import numpy as np
import sounddevice as sd

class AudioRecorder:
    def __init__(self, fs=44100, channels=1):
        self.fs = fs
        self.channels = channels
        self.chunk_size = 1024
        self._volume = 0.0
        self._running = False
        self._thread = None
        self._lock = threading.Lock()

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
  
    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()
    
    def get_volume(self):
        with self._lock:
            return self._volume
        
    def _loop(self):
        with sd.InputStream(samplerate=self.fs, channels=self.channels, blocksize=self.chunk_size) as stream:
            while self._running:
                data, _ = stream.read(self.chunk_size)
                rms = float(np.sqrt(np.mean(np.square(data))))
                with self._lock:
                    self._volume = rms