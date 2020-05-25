select mv.name from movie as mv join category as c on mv.category_id=c.id where c.name = "Fiction";
select mv.name,u.name from movie as mv join category as c on mv.category_id=c.id join user as u on mv.user_id = u.id where c.name = "Fiction" and u.name="Hio" ;
