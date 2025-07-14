import React, { useState } from 'react';

interface TextInputProps {
    onSubmit: (text: string) => void;
    isLoading?: boolean;
}

const TextInput: React.FC<TextInputProps> = ({ onSubmit, isLoading = false }) => {
    const [text, setText] = useState('');

    const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        setText(event.target.value);
    };

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (text.trim() && !isLoading) {
            onSubmit(text);
        }
    };

    const exampleTexts = [
        "Eine Katze sitzt auf dem Mond und schaut zu den Sternen.",
        "Der Roboter tanzt durch die bunte Regenbogen-Stadt.",
        "Magische Schmetterlinge fliegen durch den verzauberten Wald.",
        "Das Raumschiff gleitet sanft durch die Galaxie."
    ];

    const insertExample = (exampleText: string) => {
        setText(exampleText);
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        Dein Text für die Animation:
                    </label>
                    <textarea
                        value={text}
                        onChange={handleChange}
                        placeholder="Beschreibe was animiert werden soll... z.B. 'Eine Katze wedelt mit dem Schwanz auf dem Mond'"
                        rows={6}
                        required
                        disabled={isLoading}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-y transition duration-200"
                    />
                    <div className="mt-2 text-sm text-gray-500">
                        Zeichen: {text.length} | Wörter: {text.split(' ').filter(w => w.length > 0).length}
                    </div>
                </div>

                {/* Beispiel-Texte */}
                <div className="mb-4">
                    <p className="text-sm font-medium text-gray-700 mb-2">💡 Beispiel-Texte:</p>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                        {exampleTexts.map((example, index) => (
                            <button
                                key={index}
                                type="button"
                                onClick={() => insertExample(example)}
                                disabled={isLoading}
                                className="text-left p-2 text-sm bg-gray-50 hover:bg-gray-100 rounded border transition duration-200 disabled:opacity-50"
                            >
                                {example}
                            </button>
                        ))}
                    </div>
                </div>

                <div className="flex justify-center">
                    <button 
                        type="submit" 
                        disabled={isLoading || !text.trim()}
                                                className={`px-8 py-4 rounded-lg font-medium text-white transition duration-200 ${
                            isLoading || !text.trim() 
                                ? 'bg-gray-400 cursor-not-allowed' 
                                : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transform hover:scale-105'
                        }`}
                    >
                        {isLoading ? (
                            <div className="flex items-center">
                                <div className="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-white mr-2"></div>
                                Wird animiert...
                            </div>
                        ) : (
                            <div className="flex items-center">
                                🎬 Animation erstellen
                            </div>
                        )}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default TextInput;

