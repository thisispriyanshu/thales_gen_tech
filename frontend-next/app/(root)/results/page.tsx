import VideoDropZone from "@/components/VideoDropZone";

const ResultsPage = () => {
  return (
    <div className="flex min-h-screen flex-col items-center p-8 gap-8">
      <h1 className="text-4xl font-bold text-white">
        Upload a <span className="text-orange-500">Video</span> to see the
        results
      </h1>
      <VideoDropZone />
    </div>
  );
};

export default ResultsPage;
