<?php
get_header();
while ( have_posts() ) :
	the_post();
	if ( get_post_meta( get_the_ID(), 'wimpa_page', true ) ) :
		// New WIMPA pages: the content holds the full page layout.
		the_content();
	else :
		// Pages carried over from the earlier gwmpa.org site.
		?>
		<div class="phead"><div class="wrap"><h1><?php the_title(); ?></h1></div></div>
		<section class="legacy"><div class="wrap prose"><?php the_content(); ?></div></section>
		<?php
	endif;
endwhile;
get_footer();
