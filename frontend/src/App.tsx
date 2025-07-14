import React, { useState } from 'react';
import TextInput from './components/TextInput';
import VideoDisplay from './components/VideoDisplay';

const App: React.FC = () => {
    interface VideoData {
        url: string;
        type?: string;
        message?: string;
        // Add other video data properties as needed
    }

    const [videoData, setVideoData] = useState<VideoData | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [animationType, setAnimationType] = useState<string>('combined');

    const handleTextSubmit = async (text: string) => {
    try {
        setIsLoading(true);
        setError(null);
        
        // Verwende den kostenlosen AI Endpoint
        const response = await fetch('http://localhost:5000/api/generate-free-ai-video', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                audioText: text,
                videoDescription: text // Oder separates Feld für Video-Beschreibung
            }),
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Ein Fehler ist aufgetreten');
        }
        
        const data = await response.json();
        setVideoData(data);
        
        // Zeige Erfolg-Info
        if (data.cost === 'FREE') {
            console.log('✅ Video wurde kostenlos mit AI generiert!');
        }
        
    } catch (error) {
        console.error('Error generating video:', error);
        setError(error instanceof Error ? error.message : 'Ein unbekannter Fehler ist aufgetreten');
    } finally {
        setIsLoading(false);
    }
};

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
            <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-lg overflow-hidden">
                <div className="p-8">
                    <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">
                        🎬 Animierter Text zu Video Konverter
                    </h1>
                    
                    {/* Animation Type Selector */}
                    <div className="mb-6">
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Animations-Typ wählen:
                        </label>
                        <select
                            value={animationType}
                            onChange={(e) => setAnimationType(e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            disabled={isLoading}
                        >
                            <option value="combined">🎬 Kombiniert (Wörter + Effekte)</option>
                            <option value="text">📝 Text Animation (Typewriter)</option>
                            <option value="image">🖼️ Bild Animation (Farbverläufe)</option>
                            <option value="basic">⚡ Basis Animation (Einfach)</option>
                        </select>
                    </div>
                    
                    <TextInput onSubmit={handleTextSubmit} isLoading={isLoading} />
                    
                    {error && (
                        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                            <p className="text-red-600">{error}</p>
                        </div>
                    )}
                    
                    {isLoading && (
                        <div className="flex flex-col items-center justify-center mt-8">
                            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
                            <p className="mt-4 text-gray-600">
                                {animationType === 'combined' && '🎬 Erstelle kombinierte Animation...'}
                                {animationType === 'text' && '📝 Erstelle Text-Animation...'}
                                {animationType === 'image' && '🖼️ Erstelle Bild-Animation...'}
                                {animationType === 'basic' && '⚡ Erstelle Basis-Animation...'}
                            </p>
                        </div>
                    )}
                    
                    {!isLoading && videoData && (
                        <div className="mt-6">
                            {videoData.message && (
                                <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                                    <p className="text-green-700">✅ {videoData.message}</p>
                                    <p className="text-sm text-green-600 mt-1">
                                        🎬 Animation-Typ: {animationType}
                                    </p>
                                </div>
                            )}
                            <VideoDisplay videoData={videoData} />
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default App;
