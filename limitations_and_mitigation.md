# Limitations and mitigation

We have striven to make this system as robust as we can, nevertheless in some rare circumstances it could have difficulties transporting tubes safely. Here we discuss those situations, and the measures already in place and which can be put in place to mitigate them.

To have any success with this system you need to calibrate it correctly, as discussed in Installation.md.

The system can struggle with tubes if the following two conditions are met simultaneously:
- the label is right at the top of the uncapped tube 
- AND the label is not properly attached but hanging loosely off

If either alone is met the system should work satisfactorily.

If they are both met the tube can swing out towards the front of the robot when picked up.

This could mean that the tube could be dropped outside the rack as it is lowered, or a collision could occur.

## Avoiding this issue
- If you are labelling the tubes, don't start the label right at the top of the tube
- Ensure labels are well attached

## Mitigation of this issue
The very worst case scenario would be if a misaligned tube could cause a collision in which all the samples on a rack are destroyed/contaminated. We have implemented by default procedures that aim to avoid this possibility.
- when the tube is lowered into a rack the force of the stepper motors is reduced so that if a collision did occur little force would be exerted (you can disable this protection with `tube_mover.drop_with_low_current = False`).
- after the tube is lowered into the rack the tube homes itself and attempts to detect whether a collision has occurred. If a collision has occurred it stops (you can disable this protection with `tube_mover.home_after_drop = False`).

## Furter safety procedures you can enable
- Make sure to print `v2.2` of the rack which allows a wider range of tube positions.
- Set `tube_mover.drop_with_shake=True` to shake the tube as it is lowered, making it more likely that the center of the rack position will be found.
- Set `tube_mover.use_transit_channel=True` to make the tool never carry one tube over another, reducing the possibility of dripping

