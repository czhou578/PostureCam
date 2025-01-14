import Image from "next/image";
import WebcamFeed from "./WebcamFeed";

export default function Home() {
  return (
    <div>
      <div className="flex flex-col min-h-screen justify-center items-center">
        <h1>Posture Cam</h1>
        <WebcamFeed />
      </div>
    </div>
  );
}
