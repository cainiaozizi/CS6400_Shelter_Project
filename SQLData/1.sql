USE cs6400_su20_team07_final;

CREATE TABLE Orig_Users (
    `email` VARCHAR(25) CHARACTER SET utf8,
    `password` VARCHAR(3) CHARACTER SET utf8,
    `u_f_name` VARCHAR(10) CHARACTER SET utf8,
    `u_l_name` VARCHAR(9) CHARACTER SET utf8,
    `start_date` DATETIME,
    `phone` VARCHAR(25),
    `Volunteer` INT
);
INSERT INTO Orig_Users VALUES
    ('asmith@zotware.com','pwd','Nichelle','Ruta','2019-01-01 00:00:00',2154786705,1),
    ('barias@xx-holding.com','pwd','Layla','Boulter','2018-12-25 00:00:00',6656503829,1),
    ('cjurney@groovestreet.com','pwd','Brittni','Boord','2018-12-30 00:00:00',1875176352,1),
    ('cvonasek@toughzap.com','pwd','Malcolm','Vocelka','2018-12-26 00:00:00',3961960379,1),
    ('dkeetch@golddex.com','pwd','Roosevelt','Springe','2018-12-24 00:00:00',4531134131,1),
    ('dmontezuma@green-plus.com','pwd','Jeanice','Heintzman','2018-12-27 00:00:00',5515197966,1),
    ('edubaldi@finhigh.com','pwd','Candida','Nayar','2018-12-31 00:00:00',1787601359,1),
    ('fcrupi@rangreen.com','pwd','Gail','Fallick','2018-12-25 00:00:00',3703791448,1),
    ('gmatuszak@green-plus.com','pwd','Salome','Fern','2018-12-31 00:00:00',3731243863,1),
    ('jgiguere@openlane.com','pwd','Cory','Diestel','2018-12-23 00:00:00',7806817465,1),
    ('jsweely@fasehatice.com','pwd','Dalene','Craghead','2019-01-01 00:00:00',3875514070,1),
    ('kmunns@yearin.com','pwd','Laurel','Ahle','2018-12-31 00:00:00',5644284709,1),
    ('lmenter@plexzap.com','pwd','Roselle','Emigh','2018-12-23 00:00:00',8947815589,1),
    ('mdeleo@funholding.com','pwd','Quentin','Loader','2018-12-29 00:00:00',8795863139,1),
    ('mmallett@konex.com','pwd','Angella','Hoogland','2018-12-26 00:00:00',4386427372,1),
    ('mo@burdell.com','mo','Mo','Burdell','2018-01-01 00:00:00',7807479196,0),
    ('nbatman@ron-tech.com','pwd','Raylene','Blackwood','2018-12-29 00:00:00',7651019389,1),
    ('ncoyier@funholding.com','pwd','Daniel','Neither','2018-12-26 00:00:00',8389088169,1),
    ('rdiestel@goodsilron.com','pwd','Ronny','Tagala','2018-12-30 00:00:00',5301442835,1),
    ('sahle@treequote.com','pwd','Lettie','Colla','2018-12-30 00:00:00',7962203632,1),
    ('sjurney@groovestreet.com','pwd','Evangelina','Crupi','2018-12-26 00:00:00',4931010544,1),
    ('smaclead@openlane.com','pwd','Casie','Comnick','2018-12-30 00:00:00',4275104007,1),
    ('srodefer@ontomedia.com','pwd','Paris','Yum','2018-12-30 00:00:00',5323782223,1),
    ('tmarrier@hottechi.com','pwd','Herminia','Nicka','2018-12-24 00:00:00',6652890833,1),
    ('vmenter@silis.com','pwd','Nickolas','Gochal','2018-12-29 00:00:00',5660399052,1),
    ('walbares@conecom.com','pwd','Vilma','Marrier','2018-12-23 00:00:00',3419223914,1);
