<?php
get_header();
?>
<div class="phead"><div class="wrap"><h1><?php echo is_singular() ? esc_html( get_the_title() ) : esc_html( wp_get_document_title() ); ?></h1></div></div>
<section class="legacy"><div class="wrap prose">
<?php
if ( have_posts() ) :
	while ( have_posts() ) :
		the_post();
		if ( ! is_singular() ) :
			?>
			<h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
			<?php
			the_excerpt();
		else :
			the_content();
		endif;
	endwhile;
else :
	echo '<p>Nothing found.</p>';
endif;
?>
</div></section>
<?php
get_footer();
