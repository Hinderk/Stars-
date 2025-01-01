#!/usr/bin/awk -f

/enable-background/	{ next }

/<polygon/		{ printf( "<polygon\n" ) ; }
/<circle/		{ printf( "<circle\n" ) ; }
/<path/			{ printf( "<path\n" ) ; }
/style/			{ print }
/points=/		{ print ; printf( "/>\n" ) ; }
/^[[:space:]]+cx=/	{ print }
/^[[:space:]]+cy=/	{ print }
/^[[:space:]]+d=/	{ print ; printf( "/>\n" ) ; }
/^[[:space:]]+r=/	{ print ; printf( "/>\n" ) ; }


BEGIN	{
  printf( "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n" ) ;
  printf( "<svg\n" ) ;
  printf( "  version=\"1.1\"\n" ) ;
  printf( "  viewBox=\"0 1625 400 400\"\n" ) ;
  printf( "  xmlns=\"http://www.w3.org/2000/svg\">\n" ) ;
  printf( "<g fill=\"none\">\n" ) ;
}

END	{
  printf( "</g>\n" ) ;
  printf( "</svg>\n" ) ;
}
