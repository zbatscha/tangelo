const boxes = document.querySelectorAll('.box');
const rows = document.querySelectorAll('.row');

let draggedBox = null;

for (let i = 0; i < boxes.length; i++) {
    const box = boxes[i];

    box.addEventListener('dragstart', function () {
        console.log('Drag start!');
        draggedBox = box;
        setTimeout(function () {
            box.style.display = 'none';
        }, 0);
    });

    box.addEventListener('dragend', function () {
        console.log('Drag End');
        setTimeout(function () {
            draggedBox.style.display = 'block'
            draggedBox = null;
        }, 0);
    });

    for (let j = 0; j < rows.length; j++) {
        const row = rows[j];
        
        row.addEventListener('dragover', function(e) {
            e.preventDefault();
        });
        row.addEventListener('dragenter', function (e) {
            e.preventDefault();
        });
        row.addEventListener('drop', function (e) {
            console.log('drop');
            row.append(draggedBox);
        });
    }
}