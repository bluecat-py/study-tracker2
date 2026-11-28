"use strict";

const state = {
    today: null,
    history: null,
    subjects: [],
};

const $ = (selector) => document.querySelector(selector);

function el(tag, props = {}, ...children) {
    const node = document.createElement(tag);
    for (const [key, value] of Object.entries(props)) {
        if (key === "class") node.className = value;
        else if (key === "text") node.textContent = value;
        else node.setAttribute(key, value);
    }
    node.append(...children);
    return node;
}

function formatMinutes(total) {
    const hours = Math.floor(total / 60);
    const minutes = total % 60;
    if (hours === 0) return `${minutes}m`;
    if(minutes === 0) return `${hours}h`;
    return `${hours}h ${minutes}m`; 
}

function formatClock(totalSeconds) {
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;
    const ss = String(seconds).padStart(2, "0");
    if (hours === 0) return `${minutes}:${ss}`;
    return `${hours}:${String(minutes).padStart(2, "0")}:${ss}`;
}

function plural(count, word) {
    return `${count} ${word}${count === 1 ? "" : "s"}`;
}

