function confirm_delete() {
    let msg = 'To delete user, write "DELETE"';
    while (prompt(msg) !== 'DELETE');
    window.location.replace('/crud/delete/user/' + profile_user_id);
}