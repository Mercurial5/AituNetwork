$('.comment-toggle').on('click', function () {
    let comment_input = $(this).parent().parent().parent().find('.comment-input')
    console.log(comment_input)
    comment_input.toggle()
})

$('.comment-form').on('submit', function () {
    let post = $(this).parent().parent().parent();
    let post_id = post.attr('id').replace('post-', '');
    let textarea = $(this).find('textarea')

    let text = textarea.val();
    textarea.val('')

    let comment_section = $(this).parent().parent().find('.comments-section')
    generate_comment(comment_section, post_id, text)
    save_comment(post_id, current_user, text)

    return false;
})

function generate_comment(comment_section, post_id, text) {
    $.ajax({
        url: '/utils/generate-comment',
        method: 'POST',
        data: {
            author_id: current_user,
            post_id: post_id,
            user_id: current_user,
            text: text
        },
        success: function (data) {
            comment_section.append(data);
        }
    })
}

function save_comment(post_id, author_id, text) {
    $.ajax({
        url: '/users/add/comment',
        method: 'POST',
        data: {
            post_id: post_id,
            author_id: author_id,
            text: text
        }
    })
}