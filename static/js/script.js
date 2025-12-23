// TAB SWITCHING
function switchTab(tabId) {
    document.querySelectorAll('.panel').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.sidebar-btn').forEach(el => el.classList.remove('active'));
    
    document.getElementById(tabId).classList.add('active');
    
    if(tabId === 'encrypt-tab') document.getElementById('btn-encrypt').classList.add('active');
    else document.getElementById('btn-decrypt').classList.add('active');
}

// TOGGLE INPUT TYPE (FILE vs TEXT)
function toggleInput(type) {
    document.getElementById('input_type').value = type;
    
    // Update Buttons
    document.querySelectorAll('.toggle-btn').forEach(btn => btn.classList.remove('active'));
    event.currentTarget.classList.add('active'); // Highlight clicked button

    // Show/Hide Sections
    if (type === 'file') {
        document.getElementById('file-input-group').style.display = 'block';
        document.getElementById('text-input-group').style.display = 'none';
        // Remove 'required' from text, Add to file
        document.querySelector('textarea[name="secret_text"]').required = false;
        document.querySelector('input[name="file"]').required = true;
    } else {
        document.getElementById('file-input-group').style.display = 'none';
        document.getElementById('text-input-group').style.display = 'block';
        // Remove 'required' from file, Add to text
        document.querySelector('input[name="file"]').required = false;
        document.querySelector('textarea[name="secret_text"]').required = true;
    }
}

function showLoading(form) {
    const btn = form.querySelector('button[type="submit"]');
    btn.classList.add('loading');
}

// FILE NAME PREVIEW
document.querySelectorAll('input[type="file"]').forEach(input => {
    input.addEventListener('change', (e) => {
        const fileName = e.target.files[0]?.name;
        if(fileName) {
            const label = input.closest('label');
            const textStrong = label.querySelector('.text strong');
            if(textStrong) {
                textStrong.innerHTML = `<i class="fa-solid fa-check" style="color:#2563eb"></i> ${fileName}`;
            }
        }
    });
});

// DRAG AND DROP LOGIC
const img = document.getElementById("share2");
if (img) {
    let isDown = false, offset = [0,0];

    const start = (e) => {
        isDown = true;
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        offset = [img.offsetLeft - clientX, img.offsetTop - clientY];
        img.style.cursor = 'grabbing';
    };

    const end = () => { isDown = false; img.style.cursor = 'grab'; };

    const move = (e) => {
        if (!isDown) return;
        if(e.preventDefault) e.preventDefault();
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        img.style.left = (clientX + offset[0]) + 'px';
        img.style.top  = (clientY + offset[1]) + 'px';
    };

    img.addEventListener('mousedown', start);
    img.addEventListener('touchstart', start);
    document.addEventListener('mouseup', end);
    document.addEventListener('touchend', end);
    document.addEventListener('mousemove', move);
    document.addEventListener('touchmove', move, { passive: false });
}