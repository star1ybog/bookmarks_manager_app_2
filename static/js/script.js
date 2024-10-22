// static/js/script.js
$(document).ready(function () {
    // Function to render bookmarks by category
    function renderBookmarks(categorizedBookmarks) {
        $('.category-block').remove(); // Clear the current view

        for (const [category, bookmarks] of Object.entries(categorizedBookmarks)) {
            const categoryBlock = $(`
                <div class="category-block">
                    <h2>${category}</h2>
                    <ul class="bookmark-list"></ul>
                </div>
            `);

            // Sort bookmarks by title before adding them
            bookmarks.sort((a, b) => a.title.localeCompare(b.title));

            bookmarks.forEach(bookmark => {
                categoryBlock.find('.bookmark-list').append(`
                    <li data-id="${bookmark.id}">
                        <a href="${bookmark.url}" target="_blank">${bookmark.title}</a>
                        <a href="/bookmark/${bookmark.id}">View</a>
                        <button class="delete-btn">Delete</button>
                    </li>
                `);
            });

            $('body').append(categoryBlock);
        }
    }

    // Add a new bookmark
    $('#bookmark-form').on('submit', function (e) {
        e.preventDefault();
        const title = $('#title').val();
        const url = $('#url').val();
        const category = $('#category').val();

        $.ajax({
            type: 'POST',
            url: '/bookmark',
            contentType: 'application/json',
            data: JSON.stringify({ title, url, category }),
            success: function (newBookmark) {
                // Fetch updated categorized bookmarks
                $.get('/', function (html) {
                    const newDom = $(html);
                    const categorizedBookmarks = newDom.find('.category-block');
                    renderBookmarks(categorizedBookmarks);
                });
                $('#bookmark-form')[0].reset();
            }
        });
    });

    // Delete a bookmark
    $('body').on('click', '.delete-btn', function () {
        const id = $(this).closest('li').data('id');
        $.ajax({
            type: 'DELETE',
            url: `/bookmark/${id}`,
            success: function () {
                $(`li[data-id="${id}"]`).remove();
            }
        });
    });
    
    // Handle edit bookmark form submission
    $('#edit-bookmark-form').on('submit', function (e) {
        e.preventDefault();
        
        const bookmarkId = $('#bookmark-id').val();
        const title = $('#edit-title').val();
        const url = $('#edit-url').val();
        const category = $('#edit-category').val();

        $.ajax({
            type: 'PUT',
            url: `/bookmark/${bookmarkId}`,
            contentType: 'application/json',
            data: JSON.stringify({ title, url, category }),
            success: function (updatedBookmark) {
                console.log('Bookmark updated:', updatedBookmark);
                // Optionally redirect to the index or update the displayed bookmark
                window.location.href = '/'; // Redirect to the main bookmarks page
            },
            error: function (error) {
                console.error('Error updating bookmark:', error);
                alert('Error updating bookmark. Please try again.');
            }
        });
    });
});
