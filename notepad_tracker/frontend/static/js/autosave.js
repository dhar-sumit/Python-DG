// frontend/static/js/autosave.js
let timeout = null;
let fileConfirmed = false;

// DOM Elements
const filepathInput = document.getElementById('filepath');
const editor = document.getElementById('editor');
const editorSection = document.getElementById('editor-section');

// sdada
// async function handleFilePath(path) {
//   path = path.trim();
//   if (!path) {
//     showToast('Please enter a valid path.', 'error');
//     return;
//   }

//   try {
//     const res = await fetch('/check_path', {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify({ path })
//     });
//     const data = await res.json();

//     if (data.status === 'file') {
//       // Existing file - load contents
//       await loadFileContent(path);
//     } else if (data.status === 'directory') {
//       // Directory - ask user for filename inside it
//       let filename = prompt("This is a directory. Enter filename to create inside it:", "note.txt");
//       if (filename) {
//         path = path.endsWith('/') || path.endsWith('\\') ? path + filename : path + '/' + filename;
//         filepathInput.value = path;
//         await loadFileContent(path, true); // load with "new file" option
//       } else {
//         showToast('File creation cancelled.', 'error');
//         return;
//       }
//     } else if (data.status === 'not_exist') {
//       // Path doesn't exist - confirm creation
//       const create = confirm("Path doesn't exist. Create a new file at this path?");
//       if (create) {
//         filepathInput.value = path;
//         await loadFileContent(path, true);
//       } else {
//         return;
//       }
//     } else {
//       showToast('Unexpected response: ' + JSON.stringify(data), 'error');
//     }

//     editorSection.style.display = 'block';
//     fileConfirmed = true;
//     filepathInput.disabled = true;
//     editor.focus();

//   } catch (err) {
//     showToast('Error checking path: ' + err, 'error');
//   }
// }

async function checkPathStatus(path) {
  try {
    const res = await fetch('/check_path', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path })
    });
    return await res.json();
  } catch (err) {
    showToast('Error checking path: ' + err, 'error');
    return { status: 'error' };
  }
}

function combinePath(dir, filename) {
  if (!dir.endsWith('/') && !dir.endsWith('\\')) {
    dir += '/';
  }
  return dir + filename;
}


function finalizeFileSelection(path) {
  filepathInput.value = path;
  fileConfirmed = true;
  filepathInput.disabled = true;
  editorSection.style.display = 'block';
  editor.focus();
}


async function handleFilePath(path) {
  path = path.trim();
  if (!path) {
    showToast('Please enter a valid path.', 'error');
    return;
  }

  const data = await checkPathStatus(path);

  if (data.status === 'file') {
    await loadFileContent(path);
    finalizeFileSelection(path);

  } else if (data.status === 'directory') {
    let filename = prompt("This is a directory. Enter filename to open/create inside it:", "note.txt");
    if (!filename) {
      showToast('File creation cancelled.', 'error');
      return;
    }

    const fullPath = combinePath(path, filename);
    const checkFull = await checkPathStatus(fullPath);

    if (checkFull.status === 'file') {
      await loadFileContent(fullPath);
    } else {
      await loadFileContent(fullPath, true);
    }

    finalizeFileSelection(fullPath);

  } else if (data.status === 'not_exist') {
    const confirmCreate = confirm("Path doesn't exist. Create a new file at this path?");
    if (!confirmCreate) return;

    await loadFileContent(path, true);
    finalizeFileSelection(path);

  } else {
    showToast('Unexpected response: ' + JSON.stringify(data), 'error');
  }
}



// Show textarea when user confirms a valid filepath
filepathInput.addEventListener('keypress', async function (e) {
  if (e.key === 'Enter') {
    const path = filepathInput.value.trim();
    await handleFilePath(path);
  }
});

// Helper to load file content or start new file
async function loadFileContent(filepath, isNewFile = false) {
  if (isNewFile) {
    editor.value = '';
    return;
  }

  try {
    const res = await fetch('/load', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ filepath })
    });
    const data = await res.json();

    if (data.status === 'success') {
      editor.value = data.content;
    } else if (data.status === 'error' && data.message.includes('not exist')) {
      editor.value = '';
    } else {
      showToast('Error loading file: ' + data.message, 'error');
      editor.value = '';
    }
  } catch (err) {
    showToast('Error loading file: ' + err, 'error');
    editor.value = '';
  }
}

// Auto-save logic with debounce
editor.addEventListener('input', () => {
  if (!fileConfirmed) return;

  clearTimeout(timeout);
  timeout = setTimeout(() => {
    const content = editor.value.trim();
    const filepath = filepathInput.value.trim();

    if (content.length === 0) return; // Don't save empty content

    fetch('/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content, filepath }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === 'success') {
          // When save success:
          showToast('File saved successfully!', 'success');
          console.log('Saved to:', data.filepath);
        } else {
          // When save error:
          showToast('Failed to save file: ' + data.message, 'error');
          console.error('Error:', data.message);
        }
      })
      .catch((err) => {
        // When request fails:
        showToast('Failed to save file: ' + data.message, 'error');
        console.error('Request failed:', err);
      });
  }, 5000); // 5s debounce
});

// Toast notification helper
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  toast.classList.add('toast', type);
  toast.textContent = message;

  // Remove toast on click
  toast.addEventListener('click', () => {
    container.removeChild(toast);
  });

  container.appendChild(toast);

  // Auto remove after 5 seconds (matches fadeOut animation)
  setTimeout(() => {
    if (container.contains(toast)) {
      container.removeChild(toast);
    }
  }, 5000);
}
