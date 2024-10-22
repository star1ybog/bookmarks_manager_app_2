// static/js/script.js
$(document).ready(function () {
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
            success: function (bookmark) {
                $('#bookmarks-list').append(`
                    <li data-id="${bookmark.id}">
                        <a href="${bookmark.url}" target="_blank">${bookmark.title}</a>
                        <button class="delete-btn">Delete</button>
                    </li>
                `);
                $('#bookmark-form')[0].reset();
            }
        });
    });

    // Delete a bookmark
    $('#bookmarks-list').on('click', '.delete-btn', function () {
        const id = $(this).closest('li').data('id');
        $.ajax({
            type: 'DELETE',
            url: `/bookmark/${id}`,
            success: function () {
                $(`li[data-id="${id}"]`).remove();
            }
        });
    });
});
