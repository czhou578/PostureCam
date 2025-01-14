"use client"
import React, { useEffect, useRef, useState } from "react";

const WebcamFeed: React.FC = () => {
  const videoRef = useRef<HTMLVideoElement>(null); // Video element reference
  const [devices, setDevices] = useState<MediaDeviceInfo[]>([]); // Store available devices
  const [selectedDeviceId, setSelectedDeviceId] = useState<string | null>(null); // Store selected device ID

  useEffect(() => {
    // Fetch available devices
    const getDevices = async () => {
      try {
        const deviceInfos = await navigator.mediaDevices.enumerateDevices();
        const videoDevices = deviceInfos.filter((device) => device.kind === "videoinput");
        setDevices(videoDevices);

        // Automatically select the first device if no device is selected
        if (!selectedDeviceId && videoDevices.length > 0) {
          setSelectedDeviceId(videoDevices[0].deviceId);
        }
      } catch (error) {
        console.error("Error fetching devices:", error);
      }
    };

    getDevices();
  }, [selectedDeviceId]);

  useEffect(() => {
    // Start video feed when a device is selected
    const startVideoFeed = async () => {
      if (!selectedDeviceId) return;

      try {
        const constraints = {
          video: {
            deviceId: { exact: selectedDeviceId }, // Use the selected device ID
            width: { ideal: 1280 },
            height: { ideal: 720 },
          },
          audio: false,
        };

        const stream = await navigator.mediaDevices.getUserMedia(constraints);

        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (error) {
        console.error("Error accessing webcam:", error);
        alert("Unable to access the selected webcam.");
      }
    };

    startVideoFeed();

    // Cleanup on component unmount
    return () => {
      if (videoRef.current && videoRef.current.srcObject) {
        const tracks = (videoRef.current.srcObject as MediaStream).getTracks();
        tracks.forEach((track) => track.stop());
      }
    };
  }, [selectedDeviceId]);

  return (
    <div>
      <h1>Live Webcam Feed</h1>
      <label htmlFor="camera-select">Select Camera:</label>
      <select
        id="camera-select"
        onChange={(e) => setSelectedDeviceId(e.target.value)}
        value={selectedDeviceId || ""}
      >
        {devices.map((device) => (
          <option key={device.deviceId} value={device.deviceId}>
            {device.label || `Camera ${device.deviceId}`}
          </option>
        ))}
      </select>

      <video
        ref={videoRef}
        autoPlay
        playsInline
        style={{
          width: "100%",
          maxWidth: "720px",
          border: "2px solid black",
          borderRadius: "8px",
          marginTop: "10px",
        }}
      ></video>
    </div>
  );
};

export default WebcamFeed;
