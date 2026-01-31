import React, { useEffect, useRef } from 'react';
import { Terminal } from '@xterm/xterm';
import { FitAddon } from '@xterm/addon-fit';
import { WebglAddon } from '@xterm/addon-webgl';
import { CanvasAddon } from '@xterm/addon-canvas';
import { EventsOn } from '../../wailsjs/runtime/runtime';
import { WriteToSession, ResizeSession } from '../../wailsjs/go/main/App';
import '@xterm/xterm/css/xterm.css';

interface TerminalViewProps {
    sessionId: string;
}

const TerminalView: React.FC<TerminalViewProps> = ({ sessionId }) => {
    const terminalRef = useRef<HTMLDivElement>(null);
    const xtermRef = useRef<Terminal | null>(null);
    const fitAddonRef = useRef<FitAddon | null>(null);

    useEffect(() => {
        if (!terminalRef.current) return;

        // Initialize xterm.js
        const term = new Terminal({
            cursorBlink: true,
            theme: {
                background: '#1a1b26',
                foreground: '#c0caf5',
                cursor: '#c0caf5',
                selectionBackground: '#33467c',
                black: '#15161e',
                red: '#f7768e',
                green: '#9ece6a',
                yellow: '#e0af68',
                blue: '#7aa2f7',
                magenta: '#bb9af7',
                cyan: '#7dcfff',
                white: '#a9b1d6',
            },
            fontFamily: 'JetBrains Mono, Menlo, Monaco, Consolas, "Courier New", monospace',
            fontSize: 14,
            allowProposedApi: true,
        });

        const fitAddon = new FitAddon();
        term.loadAddon(fitAddon);

        // Try WebGL first, fallback to Canvas
        try {
            term.loadAddon(new WebglAddon());
        } catch (e) {
            term.loadAddon(new CanvasAddon());
        }

        term.open(terminalRef.current);
        fitAddon.fit();

        xtermRef.current = term;
        fitAddonRef.current = fitAddon;

        // Backend -> Frontend: Listen for PTY output
        const unsubscribe = EventsOn('pty-output:' + sessionId, (data: string) => {
            term.write(data);
        });

        // Frontend -> Backend: Send data
        term.onData((data) => {
            WriteToSession(sessionId, data);
        });

        // Handle Resize
        const handleResize = () => {
            fitAddon.fit();
            const { rows, cols } = term;
            ResizeSession(sessionId, rows, cols);
        };

        window.addEventListener('resize', handleResize);

        // Initial resize to sync backend
        handleResize();

        return () => {
            unsubscribe();
            window.removeEventListener('resize', handleResize);
            term.dispose();
        };
    }, [sessionId]);

    return (
        <div className="flex-1 w-full h-full overflow-hidden bg-[#1a1b26] p-2">
            <div ref={terminalRef} className="w-full h-full" />
        </div>
    );
};

export default TerminalView;
