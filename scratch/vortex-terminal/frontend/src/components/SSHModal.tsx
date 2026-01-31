import React, { useState } from 'react';

interface SSHModalProps {
    onConnect: (host: string, user: string, pass: string, port: number) => void;
    onClose: () => void;
}

const SSHModal: React.FC<SSHModalProps> = ({ onConnect, onClose }) => {
    const [host, setHost] = useState('');
    const [user, setUser] = useState('');
    const [pass, setPass] = useState('');
    const [port, setPort] = useState(22);
    const [showPass, setShowPass] = useState(false);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onConnect(host, user, pass, port);
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
            <div className="bg-[#1f2335] border border-white/10 rounded-xl p-6 w-[400px] shadow-2xl">
                <h2 className="text-[#7dcfff] text-xl font-bold mb-4">SSH Connection</h2>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="flex space-x-2">
                        <div className="flex-1">
                            <label className="block text-xs text-[#565f89] mb-1">Host/IP Address</label>
                            <input
                                type="text"
                                value={host}
                                onChange={(e) => setHost(e.target.value)}
                                className="w-full bg-[#1a1b26] border border-white/5 rounded px-3 py-2 text-sm text-[#c0caf5] outline-none focus:border-[#7dcfff]/50"
                                placeholder="192.168.1.1"
                                required
                            />
                        </div>
                        <div className="w-24">
                            <label className="block text-xs text-[#565f89] mb-1">Port</label>
                            <input
                                type="number"
                                value={port}
                                onChange={(e) => setPort(parseInt(e.target.value))}
                                className="w-full bg-[#1a1b26] border border-white/5 rounded px-3 py-2 text-sm text-[#c0caf5] outline-none focus:border-[#7dcfff]/50"
                                required
                            />
                        </div>
                    </div>
                    <div>
                        <label className="block text-xs text-[#565f89] mb-1">Username</label>
                        <input
                            type="text"
                            value={user}
                            onChange={(e) => setUser(e.target.value)}
                            className="w-full bg-[#1a1b26] border border-white/5 rounded px-3 py-2 text-sm text-[#c0caf5] outline-none focus:border-[#7dcfff]/50"
                            placeholder="username"
                            required
                        />
                    </div>
                    <div>
                        <label className="block text-xs text-[#565f89] mb-1">Password</label>
                        <div className="relative">
                            <input
                                type={showPass ? "text" : "password"}
                                value={pass}
                                onChange={(e) => setPass(e.target.value)}
                                className="w-full bg-[#1a1b26] border border-white/5 rounded px-3 py-2 text-sm text-[#c0caf5] outline-none focus:border-[#7dcfff]/50"
                                placeholder="password"
                                required
                            />
                            <button
                                type="button"
                                onClick={() => setShowPass(!showPass)}
                                className="absolute right-3 top-2 text-[#565f89] hover:text-[#7dcfff]"
                            >
                                {showPass ? "Hide" : "Show"}
                            </button>
                        </div>
                    </div>
                    <div className="flex justify-end space-x-3 mt-6">
                        <button
                            type="button"
                            onClick={onClose}
                            className="px-4 py-2 text-sm text-[#565f89] hover:text-[#c0caf5]"
                        >Cancel</button>
                        <button
                            type="submit"
                            className="px-6 py-2 bg-[#7aa2f7] hover:bg-[#89ddff] text-[#1a1b26] text-sm font-bold rounded transition-colors"
                        >Connect</button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default SSHModal;
