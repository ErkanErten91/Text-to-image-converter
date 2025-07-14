import React, { useState } from 'react';

interface VideoTextInputProps {
    onSubmit: (audioText: string, videoDescription: string, options: any) => void;
    isLoading?: boolean;
}

const VideoTextInput: React.FC<VideoTextInputProps> = ({ onSubmit, isLoading = false }) => {
    const [audioText, setAudioText] = useState('');
    const [videoDescription, setVideoDescription] = useState('');
    const [language, setLanguage] = useState('de');
    const [style, setStyle] = useState('explainer');

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (audioText.trim() && !isLoading) {
            const options = {
                language,
                style,
                resolution: '1080p',
                voice: 'anna'
            };
            onSubmit(audioText, videoDescription || audioText, options);
        }
    };

    return (
        <div className="space-y-6">
            <form onSubmit={handleSubmit} className="space-y-4">
                {/* Audio Text */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        Text für Audio (wird gesprochen):
                    </label>
                    <textarea
                        value={audioText}
                        onChange={(e) => setAudioText(e.target.value)}
                        placeholder="Was soll gesprochen werden?"
                        rows={4}
                        required
                        disabled={isLoading}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>

                {/* Video Description */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        Video-Beschreibung (optional - für KI-Bilder):
                    </label>
                    <textarea
                        value={videoDescription}
                        onChange={(e) => setVideoDescription(e.target.value)}
                        placeholder="Beschreibe was im Video zu sehen sein soll (z.B. 'Ein sonniger Tag im Park mit Kindern')"
                        rows={3}
                        disabled={isLoading}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>

                {/* Options */}
                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Sprache:
                        </label>
                        <select
                            value={language}
                            onChange={(e) => setLanguage(e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        >
                            <option value="de">Deutsch</option>
                            <option value="en">English</option>
                            <option value="es">Español</option>
                            <option value="fr">Français</option>
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Stil:
                        </label>
                        <select
                            value={style}
                            onChange={(e) => setStyle(e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        >
                            <option value="explainer">Erklärvideo</option>
                            <option value="presentation">Präsentation</option>
                            <option value="tutorial">Tutorial</option>
                            <option value="storytelling">Storytelling</option>
                        </select>
                    </div>
                </div>

                <button 
                    type="submit" 
                    disabled={isLoading || !audioText.trim()}
                    className={`w-full py-3 rounded-lg font-medium text-white transition duration-200 ${
                        isLoading || !audioText.trim() 
                            ? 'bg-gray-400 cursor-not-allowed' 
                            : 'bg-blue-600 hover:bg-blue-700'
                    }`}
                >
                    {isLoading ? 'KI generiert Video...' : 'KI-Video generieren'}
                </button>
            </form>
        </div>
    );
};

export default VideoTextInput;
