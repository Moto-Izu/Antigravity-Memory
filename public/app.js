const feed = document.getElementById('feed');
const atomCountEl = document.getElementById('atom-count');
let atomCount = 0;

function connectSynapse() {
    const evtSource = new EventSource('/stream');

    evtSource.onmessage = function (e) {
        try {
            const data = JSON.parse(e.data);
            renderAtom(data);
        } catch (err) {
            console.error("Parse Error", err);
        }
    };

    evtSource.onerror = function () {
        console.warn("Synapse lost. Retrying...");
        evtSource.close();
        setTimeout(connectSynapse, 3000);
    };
}

function renderAtom(atom) {
    // Avoid duplicates if needed, but server tails log so it's fine.

    const card = document.createElement('div');
    card.className = 'atom-card';

    // Header
    const header = document.createElement('div');
    header.className = 'atom-header';
    header.innerHTML = `
        <span class="atom-author">@${atom.author || 'UNKNOWN'}</span>
        <span class="atom-time">${new Date(atom.timestamp).toLocaleTimeString()}</span>
    `;

    // Content
    const content = document.createElement('div');
    content.className = 'atom-content';
    content.innerText = atom.content || '';

    card.appendChild(header);
    card.appendChild(content);

    // Media
    if (atom.media && atom.media.length > 0) {
        const mediaContainer = document.createElement('div');
        mediaContainer.className = 'atom-media';
        atom.media.forEach(src => {
            const img = document.createElement('img');
            img.src = src;
            mediaContainer.appendChild(img);
        });
        card.appendChild(mediaContainer);
    }

    // Insert at top
    feed.insertBefore(card, feed.firstChild);

    // Stats
    atomCount++;
    atomCountEl.innerText = atomCount.toString().padStart(4, '0');

    // Garbage collection (keep DOM light)
    if (feed.children.length > 100) {
        feed.removeChild(feed.lastChild);
    }
}

// Boot
connectSynapse();
