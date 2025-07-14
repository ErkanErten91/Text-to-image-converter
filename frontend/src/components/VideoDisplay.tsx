import React from 'react';

interface VideoData {
    url: string;
}

interface VideoDisplayProps {
    videoData: VideoData;
}

const VideoDisplay: React.FC<VideoDisplayProps> = ({ videoData }) => {
    // Stelle sicher, dass die URL mit http://localhost:5000 beginnt, falls sie relativ ist
    const videoUrl = videoData.url.startsWith('http') 
        ? videoData.url 
        : `http://localhost:5000${videoData.url}`;

    return (
        <div className="mt-8 pt-6 border-t border-gray-200">
            <h2 className="text-2xl font-semibold text-center text-gray-800 mb-6">Dein generiertes Video</h2>
            <div className="rounded-lg overflow-hidden shadow-lg max-w-3xl mx-auto">
                <video className="w-full" controls autoPlay>
                    <source src={videoUrl} type="video/mp4" />
                    Dein Browser unterstützt das Video-Tag nicht.
                </video>
            </div>
        </div>
    );
};

export default VideoDisplay;
