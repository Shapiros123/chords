< !DOCTYPE
html >
< html
lang = "en" >
< head >
< meta
charset = "UTF-8" >
< meta
name = "viewport"
content = "width=device-width, initial-scale=1.0" >
< title > TabStudio
Pro < / title >
< style >
:root
{
    --bg - base:  # 0f172a;
        --bg - sidebar:  # 1e293b;
--bg - card:  # 1e293b;
--border - color:  # 334155;
--text - main:  # f8fafc;
--text - muted:  # 94a3b8;
--accent:  # 38bdf8;
--accent - hover:  # 0ea5e9;
}

*{
    box - sizing: border - box;
}

body
{
    margin: 0;
font - family: -apple - system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans - serif;
background - color: var(--bg - base);
color: var(--text - main);
display: flex;
height: 100
vh;
overflow: hidden;
}

/ *Sidebar * /
# sidebar {
width: 380
px;
background - color: var(--bg - sidebar);
border - right: 1
px
solid
var(--border - color);
display: flex;
flex - direction: column;
height: 100
vh;
}

.sidebar - header
{
padding: 24
px
20
px
16
px
20
px;
font - size: 18
px;
font - weight: 700;
letter - spacing: 0.5
px;
color: var(--text - main);
display: flex;
align - items: center;
justify - content: space - between;
border - bottom: 1
px
solid
var(--border - color);
}

.sidebar - header
span
{
color: var(--accent);
font - size: 12
px;
background: rgba(56, 189, 248, 0.1);
padding: 4
px
8
px;
border - radius: 6
px;
}

/ *Search
Bar * /
.search - container
{
padding: 16
px
20
px;
border - bottom: 1
px
solid
var(--border - color);
}

# search-input {
width: 100 %;
padding: 10
px
14
px;
background - color:  # 0f172a;
border: 1
px
solid
var(--border - color);
border - radius: 8
px;
color: var(--text - main);
font - size: 14
px;
outline: none;
transition: border - color
0.2
s;
}

# search-input:focus {
border - color: var(--accent);
}

/ *Song
List * /
# song-list {
flex: 1;
overflow - y: auto;
padding: 10
px
0;
}

.song - item
{
    padding: 12px 20px;
cursor: pointer;
border - bottom: 1
px
solid
rgba(51, 65, 85, 0.4);
transition: background - color
0.15
s, padding - left
0.15
s;
}

.song - item: hover
{
    background - color: rgba(56, 189, 248, 0.05);
padding - left: 24
px;
}

.song - item.active
{
    background - color: rgba(56, 189, 248, 0.1);
border - left: 4
px
solid
var(--accent);
}

.song - item
strong
{
    display: block;
color: var(--text - main);
font - size: 15
px;
margin - bottom: 3
px;
}

.song - item
span
{
    font - size: 13px;
color: var(--text - muted);
}

/ *Main
View * /
# main-view {
flex: 1;
display: flex;
flex - direction: column;
height: 100
vh;
overflow: hidden;
background - color: var(--bg - base);
}

.viewer - header
{
    padding: 20px 40px;
border - bottom: 1
px
solid
var(--border - color);
background - color: var(--bg - sidebar);
display: flex;
justify - content: space - between;
align - items: center;
}

.song - meta
h1
{
    margin: 0 0 4px 0;
font - size: 24
px;
color: var(--text - main);
}

.song - meta
h3
{
    margin: 0;
font - size: 14
px;
color: var(--text - muted);
font - weight: normal;
}

.viewer - actions
{
    display: flex;
gap: 10
px;
}

.btn
{
    background - color:  # 334155;
        color: var(--text - main);
border: none;
padding: 8
px
14
px;
border - radius: 6
px;
cursor: pointer;
font - size: 13
px;
font - weight: 600;
transition: background - color
0.2
s;
}

.btn: hover
{
    background - color:  # 475569;
}

.btn - primary
{
    background - color: var(--accent);
color:  # 0f172a;
}

.btn - primary: hover
{
    background - color: var(--accent - hover);
}

/ *Content
Area * /
.content - scroll
{
    flex: 1;
padding: 40
px;
overflow - y: auto;
}

pre
# song-content {
font - family: "Courier New", Courier, monospace;
font - size: 15
px;
line - height: 1.6;
color:  # e2e8f0;
background: var(--bg - card);
padding: 30
px;
border - radius: 12
px;
border: 1
px
solid
var(--border - color);
white - space: pre - wrap;
word - wrap:
break
-word;
margin: 0;
}

.placeholder - state
{
display: flex;
flex - direction: column;
align - items: center;
justify - content: center;
height: 100 %;
color: var(--text - muted);
text - align: center;
}

.placeholder - state
svg
{
width: 48
px;
height: 48
px;
margin - bottom: 16
px;
opacity: 0.4;
}

/ *Custom
Scrollbar * /
::-webkit - scrollbar
{
width: 6
px;
height: 6
px;
}
::-webkit - scrollbar - track
{
background: transparent;
}
::-webkit - scrollbar - thumb
{
background: var(--border - color);
border - radius: 3
px;
}
::-webkit - scrollbar - thumb: hover
{
background: var(--text - muted);
}
< / style >
    < / head >
        < body >

        <!-- Sidebar -->
< div
id = "sidebar" >
     < div


class ="sidebar-header" >


TabStudio < span
id = "song-count" > Loading... < / span >
< / div >
< div


class ="search-container" >

< input
type = "text"
id = "search-input"
placeholder = "Search by song or artist..." >
< / div >
< div
id = "song-list" > < / div >
< / div >

< !-- Main
View -->
< div
id = "main-view" >
< div


class ="viewer-header" id="viewer-header" style="display: none;" >

< div


class ="song-meta" >

< h1
id = "song-title" > < / h1 >
< h3
id = "song-artist" > < / h3 >
< / div >
< div


class ="viewer-actions" >

< button


class ="btn" onclick="adjustFontSize(1)" > A+ < / button >

< button


class ="btn" onclick="adjustFontSize(-1)" > A- < / button >

< button


class ="btn btn-primary" id="copy-btn" onclick="copyChords()" > Copy Chords < / button >

< / div >
< / div >

< div


class ="content-scroll" id="content-scroll" >

< div
id = "placeholder"


class ="placeholder-state" >

< svg
xmlns = "http://www.w3.org/2000/svg"
fill = "none"
viewBox = "0 0 24 24"
stroke = "currentColor" >
< path
stroke - linecap = "round"
stroke - linejoin = "round"
stroke - width = "2"
d = "M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" / >
< / svg >
< p > Select
a
song
from the sidebar

to
load
chords < / p >
< / div >
< pre
id = "song-content"
style = "display: none;" > < / pre >
< / div >
< / div >

< script >
let
allSongs = [];
let
currentFontSize = 15;
const
songListDiv = document.getElementById('song-list');
const
searchInput = document.getElementById('search-input');
const
viewerHeader = document.getElementById('viewer-header');
const
titleEl = document.getElementById('song-title');
const
artistEl = document.getElementById('song-artist');
const
contentEl = document.getElementById('song-content');
const
placeholderEl = document.getElementById('placeholder');
const
songCountEl = document.getElementById('song-count');

// Fetch
directory
fetch('/api/songs')
.then(res= > res.json())
.then(songs= > {
    allSongs = songs;
songCountEl.textContent = `${songs.length}
tabs
`;
renderSongList(songs);
})
.catch(() = > {
    songCountEl.textContent = 'Error';
songListDiv.innerHTML = '<div style="padding: 20px; color: #f87171;">Failed to load catalog.</div>';
});

function
renderSongList(songsToRender)
{
    songListDiv.innerHTML = '';
songsToRender.forEach(song= > {
    const
item = document.createElement('div');
item.className = 'song-item';
item.innerHTML = ` < strong >${song.Title} < / strong > < span >${song.Artist} < / span > `;

item.addEventListener('click', () = > {
    document.querySelectorAll('.song-item').forEach(el= > el.classList.remove('active'));
item.classList.add('active');

placeholderEl.style.display = 'none';
viewerHeader.style.display = 'flex';
contentEl.style.display = 'block';

titleEl.textContent = song.Title;
artistEl.textContent = song.Artist;
contentEl.textContent = "Fetching chords from Tab4U...";

fetch(` / api / scrape?url =${encodeURIComponent(song.URL)}
`)
.then(res= > res.json())
.then(data= > {
if (data.error)
{
    contentEl.textContent = "Error loading song data.";
return;
}
contentEl.textContent = data.content;

const
isHebrew = / [\u0590 -\u05FF] /.test(song.Title);
contentEl.style.direction = isHebrew ? 'rtl': 'ltr';
contentEl.style.textAlign = isHebrew ? 'right': 'left';
})
.catch(() = > {
    contentEl.textContent = "Network error loading song.";
});
});

songListDiv.appendChild(item);
});
}

// Live
Search
Filter
searchInput.addEventListener('input', (e) = > {
    const
query = e.target.value.toLowerCase();
const
filtered = allSongs.filter(song= >
           song.Title.toLowerCase().includes(query) | |
           song.Artist.toLowerCase().includes(query)
);
renderSongList(filtered);
});

// Font
Size
Adjuster
function
adjustFontSize(delta)
{
    currentFontSize = Math.max(11, Math.min(24, currentFontSize + delta));
contentEl.style.fontSize = currentFontSize + 'px';
}

// Copy
Chords
Button
function
copyChords()
{
    navigator.clipboard.writeText(contentEl.textContent).then(() = > {
    const
btn = document.getElementById('copy-btn');
btn.textContent = 'Copied!';
setTimeout(() = > btn.textContent = 'Copy Chords', 2000);
});
}
< / script >
    < / body >
        < / html>