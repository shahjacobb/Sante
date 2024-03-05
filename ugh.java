import java.lang.Math;

public class ugh
{
    public static int sumCubes(int number)
    {
        if (number == 1)
        {
            return 1;
        }

        return sumCubes(number - 1) + (int) Math.pow(number, 3);
   
    }

    public static boolean unlucky(int num)
    {
        if (num < 10)
        {
            return false;

        }

        if (num <= 100 && num >= 10)
        {
            return num / 10 % 10 + num % 10 == 13 ? true : false;
        }

        return unlucky(num / 10);

    /*
     * 67345 
     * 67345 / 10 -> unlucky(num // 10) = unlucky(6734)
     * 6734 / 10 -> unlucky(num // 10) = unlucky(673)
     * 673 / 10 -> unlucky(num // 10) = unlucky(67)
     * 
     */

    }

    public static int thirdDigit(int num)
    {
        if (num < 100) return 0;

        if (num >= 100 && num <= 1000) return num / 100 % 10;

        return thirdDigit(num / 10);
    }

    public static int sumDigit(int num)
    {
        if (num == 0) return 0;

        return sumDigit(num - 1) + num;
    }

    public static long removeOddDigits(long num)
    {
        if (num == 0) return 0;

        long lastDigit = num % 10;

        if (lastDigit % 2 == 0)
        {
            // This makes sense because we unwind the number all the way, and when we get to the base case, we need to rebuild the number. Since decimal numbers are positional, we need to shift 
            // the values left each time, creating space for the last digit each time it returns. Not doing this results in gibberish.
            return removeOddDigits(num / 10) * 10 + lastDigit;
        }
        else
        {
            return removeOddDigits(num / 10);

        }
    }

    // Remember this algorithm finds a REPEATED number, not the first repeated. So you need to calculate midpoint and look at both directions
    public static int repeatedNumberBinarySearch(int[] array)
    {
        int left = 0;
        int right = array.length - 1;

        while (left <= right)
        {
            // calculate midpoint
            int midpoint = left + (right - left) / 2;

            // you're basically just checking. if array midpoint is equal to midpoint plus 1, then we can throw away left and set left to be mid + 1. you can also choose the left side and first condition is right = med - 1
            if (array[midpoint] == array[midpoint + 1])
            left = midpoint + 1;
            
            else 
            {
                right = midpoint - 1;                
            }
            // doesn't matter which one you return
        }

        return array[midpoint];
        
        
    }

    // first bad version
    public class BadVersion extends Control {
        public int firstBadVersion(int n) {
            int left = 1, right = n, ans = -1;
            while (left <= right) {
                int mid = left + (right - left) / 2; // to avoid overflow incase (left+right)>2147483647
                if (isBadVersion(mid)) {
                    ans = mid; // record mid as current answer
                    right = mid - 1; // try to find smaller version in the left side
                } else {
                    left = mid + 1; // try to find in the right side
                }
            }
            return ans;
        }
    }
    
    public static void main(String[] args)
    {
        
        System.out.println(sumCubes(5));
        System.out.println(unlucky(673));

        System.out.println("Third Digit test");
        
        System.out.println("105: " + thirdDigit(105));
        System.out.println("756485478: " + thirdDigit(756485478));
        System.out.println("43432432: " + thirdDigit(43432432));
        
        
        System.out.println("Sum Digit, 5:" + sumDigit(5));
        System.out.println("Sum Digit, 3:" + sumDigit(3));
        
        
        System.out.println("Remove Odds Test");
        
        System.out.println("Remove Odds 343434343438:" + removeOddDigits(343434343438l));
        System.out.println("Remove Odds 7777777777777777:" + removeOddDigits(7777777777777777l));
        System.out.println("Remove Odds 52525252:" + removeOddDigits(52525252));

   



        

    }
}