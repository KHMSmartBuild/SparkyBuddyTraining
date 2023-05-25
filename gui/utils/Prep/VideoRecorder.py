import cv2
import threading

class VideoRecorder:
    def __init__(self, output_file):
        self.output_file = output_file
        self.is_recording = False
        self.thread = None

    def start_recording(self):
        self.is_recording = True
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def stop_recording(self):
        self.is_recording = False
        if self.thread is not None:
            self.thread.join()
            self.thread = None

    def _record(self):
        cap = cv2.VideoCapture(0)  # Use the default camera
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(self.output_file, fourcc, fps, (width, height))

        while self.is_recording:
            ret, frame = cap.read()
            if ret:
                out.write(frame)
                cv2.imshow('Recording', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()
