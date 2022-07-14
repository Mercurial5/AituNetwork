function confirm_delete() {
    let msg = prompt('To delete user, write "DELETE"');

    if (msg === 'DELETE') window.location.replace('/crud/delete/user/' + profile_user_id);
    else console.log(msg);
}