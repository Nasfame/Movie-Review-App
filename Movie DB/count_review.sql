select count(*),mv.name from review join movie as mv on review.movie_id=mv.id group by mv.name;
