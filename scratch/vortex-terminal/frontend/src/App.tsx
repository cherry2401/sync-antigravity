import React, { useState, useEffect } from 'react';
import { CreateLocalSession, CreateSSHSession, CloseSession } from '../wailsjs/go/main/App';
import TerminalView from './components/TerminalView';
import SSHModal from './components/SSHModal';

interface Tab {
    id: string;
    title: string;
    sessionId: string;
}

const App: React.FC = () => {
    const [tabs, setTabs] = useState<Tab[]>([]);
    const [activeTabId, setActiveTabId] = useState<string | null>(null);
    const [showSSHModal, setShowSSHModal] = useState(false);

    const addNewTab = async (title = "PowerShell") => {
        // Default rows/cols, TerminalView will resize on mount
        const sessionId = await CreateLocalSession("powershell.exe", 24, 80);
        if (!sessionId) return;

        const newId = Math.random().toString(36).substring(7);
        const newTab: Tab = { id: newId, title, sessionId };

        setTabs(prev => [...prev, newTab]);
        setActiveTabId(newId);
    };

    const handleSSHConnect = async (host: string, user: string, pass: string, port: number) => {
        const sessionId = await CreateSSHSession(host, user, pass, port, 24, 80);
        if (!sessionId) {
            alert("Failed to connect via SSH");
            return;
        }

        const newId = Math.random().toString(36).substring(7);
        const newTab: Tab = { id: newId, title: "SSH: " + host, sessionId };

        setTabs(prev => [...prev, newTab]);
        setActiveTabId(newId);
        setShowSSHModal(false);
    };

    const closeTab = (id: string, sessionId: string) => {
        CloseSession(sessionId);
        const newTabs = tabs.filter(t => t.id !== id);
        setTabs(newTabs);
        if (activeTabId === id) {
            setActiveTabId(newTabs.length > 0 ? newTabs[newTabs.length - 1].id : null);
        }
    };

    useEffect(() => {
        // Initial tab
        if (tabs.length === 0) {
            addNewTab();
        }
    }, []);

    return (
        <div className="flex flex-col h-screen select-none">
            {/* Titlebar */}
            <div className="flex items-center bg-[#1a1b26] border-b border-white/5 h-10 w-full" style={{ "--wails-draggable": "drag" } as any}>
                <div className="flex flex-1 overflow-x-auto no-scrollbar ml-2 space-x-1">
                    {tabs.map(tab => (
                        <div
                            key={tab.id}
                            onClick={() => setActiveTabId(tab.id)}
                            className={`flex items-center h-8 px-4 text-xs rounded-t-md cursor-pointer transition-colors max-w-[150px] group
                                ${activeTabId === tab.id ? 'bg-[#24283b] text-[#7dcfff]' : 'text-[#565f89] hover:bg-white/5'}`}
                            style={{ "--wails-draggable": "no-drag" } as any}
                        >
                            <span className="truncate mr-2">{tab.title}</span>
                            <span
                                onClick={(e) => { e.stopPropagation(); closeTab(tab.id, tab.sessionId); }}
                                className="opacity-0 group-hover:opacity-100 hover:text-red-400 font-bold"
                            >×</span>
                        </div>
                    ))}
                    <button
                        onClick={() => addNewTab()}
                        className="flex items-center justify-center w-8 h-8 text-[#565f89] hover:bg-white/5 rounded-full"
                        style={{ "--wails-draggable": "no-drag" } as any}
                    >+</button>
                    <button
                        onClick={() => setShowSSHModal(true)}
                        className="flex items-center justify-center px-2 h-8 text-[#565f89] hover:bg-white/5 rounded text-[10px] font-bold"
                        style={{ "--wails-draggable": "no-drag" } as any}
                    >SSH</button>
                </div>

                {/* Window Controls */}
                <div className="flex h-full items-center mr-2 space-x-3" style={{ "--wails-draggable": "no-drag" } as any}>
                    <div className="w-3 h-3 rounded-full bg-yellow-500/50 hover:bg-yellow-500 cursor-pointer" onClick={() => (window as any).runtime.WindowMinimise()}></div>
                    <div className="w-3 h-3 rounded-full bg-green-500/50 hover:bg-green-500 cursor-pointer" onClick={() => (window as any).runtime.WindowToggleMaximise()}></div>
                    <div className="w-3 h-3 rounded-full bg-red-500/50 hover:bg-red-500 cursor-pointer" onClick={() => (window as any).runtime.Quit()}></div>
                </div>
            </div>

            {/* Main Terminal View */}
            <div className="flex-1 relative bg-[#1a1b26]">
                {tabs.map(tab => (
                    <div key={tab.id} className={activeTabId === tab.id ? 'h-full' : 'hidden'}>
                        <TerminalView sessionId={tab.sessionId} />
                    </div>
                ))}
                {tabs.length === 0 && (
                    <div className="flex items-center justify-center h-full text-[#565f89]">
                        No active sessions. Click + to start.
                    </div>
                )}
            </div>

            {showSSHModal && (
                <SSHModal
                    onConnect={handleSSHConnect}
                    onClose={() => setShowSSHModal(false)}
                />
            )}
        </div>
    );
};

export default App;
